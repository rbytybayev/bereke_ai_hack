import httpx
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.models.sanctions import Sanction
from io import BytesIO

# Примеры источников (можно заменить на реальные)
OFAC_URL = "https://www.treasury.gov/ofac/downloads/sdn.csv"
EU_URL = "https://data.europa.eu/data/datasets/consolidated-list-sanctions?format=csv"

async def refresh_ofac(session: AsyncSession):
    async with httpx.AsyncClient() as client:
        r = await client.get(OFAC_URL)
        r.raise_for_status()
        df = pd.read_csv(BytesIO(r.content))

    await session.execute(delete(Sanction).where(Sanction.source == "OFAC"))
    for _, row in df.iterrows():
        sanction = Sanction(
            source="OFAC",
            name=str(row.get("Name", "")),
            original_name=str(row.get("Alternate Names", "")),
            comment=str(row.get("Remarks", "")),
        )
        session.add(sanction)
    await session.commit()


async def refresh_eu(session: AsyncSession):
    async with httpx.AsyncClient() as client:
        r = await client.get(EU_URL)
        r.raise_for_status()
        df = pd.read_csv(BytesIO(r.content))

    await session.execute(delete(Sanction).where(Sanction.source == "EU"))
    for _, row in df.iterrows():
        sanction = Sanction(
            source="EU",
            name=str(row.get("Name", "")),
            original_name=str(row.get("Alias", "")),
            comment=str(row.get("Program", "")),
        )
        session.add(sanction)
    await session.commit()


async def refresh_all_sanctions(session: AsyncSession):
    await refresh_ofac(session)
    await refresh_eu(session)
