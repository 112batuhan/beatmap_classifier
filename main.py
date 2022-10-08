from custom_exception import EmptyMapDownloadError
from api_utils import Predicter
from fastapi import FastAPI, Path, HTTPException
import json

predicter = Predicter()
app = FastAPI()


@app.get("/beatmap_category/{beatmap_id}")
async def return_all_values(beatmap_id: int = Path(title="Id of the beatmap.")):
    try:
        result = predicter.predict(beatmap_id, complete_eval=True)
        return result
    except EmptyMapDownloadError:
        raise HTTPException(
            status_code=404, detail="The requested map is not a valid map")
