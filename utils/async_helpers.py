from typing import Optional
import asyncio


async def send_appointment_notification(
    patient_name: str,
    slot: str,
    channel: str = "sms"
) -> None:
    
    await asyncio.sleep(0.1) 

    print(
        f"[{channel.upper()}] Sent to "
        f"{patient_name}: Appointment at {slot} confirmed"
    )


async def send_cancellation_notification(
    patient_name: str,
    slot: str,
) -> None:

    await asyncio.sleep(0.1)

    print(
        f"[SMS] Sent to "
        f"{patient_name}: Appointment at {slot} has been cancelled"
    )