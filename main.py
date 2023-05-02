import os
import uvicorn

from bot_utils.bot import sender
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from request_utils.request_config import HOST, PORT, ALERT_DESTINATION, MAX_STRLEN
from typing import Dict, List


def get_answer_from_annotations(annotations: Dict[str, str]) -> str:
    to_ret = ""
    for key, val in annotations.items():
        if len(val) > MAX_STRLEN:
            val = val[:MAX_STRLEN] + "   ...too long to display full"
        to_ret += "{} : {}\n".format(key, val)
    return to_ret


class Alert(BaseModel):
    status: str = Field(default={})
    generator_url: str = Field(
        alias="generatorURL",
        default={},
    )
    annotations: Dict[str, str]
    labels: Dict[str, str] = Field(
        default={},
    )

    specific_annotations: Dict[str, str] = Field(
        default={},
    )


class AlertGroup(BaseModel):
    receiver: str = Field()
    status: str = Field()
    group_key: str = Field(
        alias="groupKey",
        default={}
    )
    group_labels: Dict[str, str] = Field(
        alias="groupLabels",
        default={},
    )
    common_annotations: Dict[str, str] = Field(
        alias="commonAnnotations",
        default={},
    )
    common_labels: Dict[str, str] = Field(
        alias="commonLabels",
        default={},
    )
    alerts: List[Alert] = Field(
        default={},
    )


app = FastAPI()


@app.post(ALERT_DESTINATION)
async def receive_alert(request: Request, alert_group: AlertGroup):
    if len(alert_group.alerts) == 0:
        return
    sender("DOBROYE UTRO, RECEIVED ALERT(s), annotations:\n")
    sender("receiver : {}\n".format(alert_group.receiver))
    sender("status : {}\n".format(alert_group.status))
    for alert_item in alert_group.alerts:
        if alert_item.status == "resolved":
            sender("resolved alert!\n")
            continue
        sender(get_answer_from_annotations(alert_item.annotations))


def main():
    uvicorn.run("main:app", host=HOST, port=int(os.environ.get('PORT', PORT)), log_level="info")


if __name__ == "__main__":
    main()
