#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Created on Sun Feb 18 2024 13:48:55 by codeskyblue
"""


import io
from pathlib import Path
import platform
from typing import List

from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app_inspector.model import DeviceInfo, Hierarchy, ShellResponse
from app_inspector.provider import AndroidProvider


app = FastAPI()


class InfoResponse(BaseModel):
    version: str
    description: str
    platform: str
    code_language: str


@app.get("/info")
def info() -> InfoResponse:
    """Information about the application"""
    return InfoResponse(
        version="0.0.1",
        description="This is a simple FastAPI application",
        platform=platform.system(),  # Linux | Darwin | Windows
        code_language="Python",
    )

@app.get("/demo")
def demo() -> str:
    """Demo endpoint"""
    static_dir = Path(__file__).parent / "static"
    print(static_dir / "demo.html")
    return FileResponse(static_dir / "demo.html")


android_provider = AndroidProvider()


@app.get("/list/android")
def android_list() -> List[DeviceInfo]:
    """List of Android devices"""
    try:
        return android_provider.list_devices()
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=500)
    

class AndroidShellPayload(BaseModel):
    command: str


@app.post("/android/{serial}/shell")
def android_shell(serial: str, payload: AndroidShellPayload) -> ShellResponse:
    """Run a shell command on an Android device"""
    try:
        driver = android_provider.get_device_driver(serial)
        return driver.shell(payload.command)
    except Exception as e:
        return ShellResponse(output="", error=str(e))


@app.get(
    "/android/{serial}/screenshot/{id}",
    responses={200: {"content": {"image/png": {}}}},
    response_class=Response,
)
def android_screenshot(serial: str, id: int) -> Response:
    """Take a screenshot of an Android device """
    try:
        driver = android_provider.get_device_driver(serial)
        pil_img = driver.screenshot(id)
        buf = io.BytesIO()
        pil_img.save(buf, format="JPEG")
        image_bytes = buf.getvalue()
        return Response(content=image_bytes, media_type="image/jpeg")
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=500)


@app.get("/android/{serial}/hierarchy")
def android_hierarchy(serial: str) -> Hierarchy:
    """Dump the view hierarchy of an Android device"""
    try:
        driver = android_provider.get_device_driver(serial)
        return driver.dump_hierarchy()
    except Exception as e:
        return Response(content=str(e), media_type="text/plain", status_code=500)