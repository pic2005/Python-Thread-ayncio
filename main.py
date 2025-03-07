import asyncio
import time
import asyncio
import time
import random
import logging
from concurrent.futures import ThreadPoolExecutor  
from queue import PriorityQueue  # ✅ เพิ่มบรรทัดนี้



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


async def main():
    users = [1, 2, 3, 4, 5]
    messages = [
        (1, "Urgent: System maintenance!"),  # ความสำคัญสูง
        (3, "Hello!"),
        (2, "Reminder!"),
        (3, "New message!"),
        (1, "Security alert!"),
    ]

    status_results = {}
    with ThreadPoolExecutor() as executor:
        results = executor.map(check_user_status, users)

    for user_id, status in zip(users, results):
        status_results[user_id] = status

    pq = PriorityQueue()

    for priority, message in messages:
        pq.put((priority, message))

    tasks = []
    while not pq.empty():
        _, message = pq.get()
        for user_id in users:
            if status_results[user_id] == "online":
                tasks.append(send_notification(user_id, message))

    await asyncio.gather(*tasks)


# รันโปรแกรม
if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time} seconds")