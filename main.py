import asyncio
import threading
import time
import random

# ส่วนของ asyncio: ส่งข้อความแจ้งเตือน (I/O-bound)
async def send_notification(user_id, message):
    print(f"Sending notification to user {user_id}: {message}")
    await asyncio.sleep(1)  # จำลองการส่งข้อความที่ใช้เวลา
    print(f"Notification sent to user {user_id}")

# ส่วนของ threading: ตรวจสอบสถานะผู้ใช้ (CPU-bound)
def check_user_status(user_id):
    print(f"Checking status of user {user_id}")
    time.sleep(2)  # จำลองการตรวจสอบสถานะที่ใช้เวลา
    status = "online" if random.choice([True, False]) else "offline"
    print(f"User {user_id} is {status}")
    return status

# ฟังก์ชันหลัก
async def main():
    users = [1, 2, 3, 4, 5]  # รายการผู้ใช้
    messages = ["Hello!", "New message!", "Reminder!", "Update available!", "Please check your inbox!"]

    # สร้าง threads เพื่อตรวจสอบสถานะผู้ใช้
    threads = []
    status_results = {}

    for user_id in users:
        thread = threading.Thread(target=lambda u=user_id: status_results.update({u: check_user_status(u)}))
        threads.append(thread)
        thread.start()

    # รอให้ threads ทั้งหมดทำงานเสร็จ
    for thread in threads:
        thread.join()

    # ส่งข้อความแจ้งเตือนให้ผู้ใช้ที่ออนไลน์
    tasks = []
    for user_id in users:
        if status_results[user_id] == "online":
            message = random.choice(messages)
            tasks.append(send_notification(user_id, message))

    await asyncio.gather(*tasks)

# รันโปรแกรม
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")