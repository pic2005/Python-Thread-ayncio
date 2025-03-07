import asyncio
import time
import random
from concurrent.futures import ThreadPoolExecutor
from queue import PriorityQueue

def send_notification_in_thread(user_id, message):
    print(f"📩 ส่งข้อความแจ้งเตือนถึงผู้ใช้ {user_id}: {message}")
    time.sleep(1)  # จำลองการส่งข้อความที่ใช้เวลา
    print(f"✅ ส่งข้อความถึงผู้ใช้ {user_id} แล้ว")

async def check_user_status_async(user_id):
    print(f"🔍 กำลังตรวจสอบสถานะของผู้ใช้ {user_id}...")
    await asyncio.sleep(2)  
    status = "online" if random.choice([True, False]) else "offline"  # สุ่มสถานะผู้ใช้
    print(f"🟢 ผู้ใช้ {user_id} อยู่ในสถานะ {status}")
    return status

# ฟังก์ชันหลัก
async def main():
    users = [1, 2, 3, 4, 5]  
    messages = [
        (1, "🚨 ด่วน! มีการอัปเดตระบบที่สำคัญ"),
        (3, "👋 สวัสดี! วันนี้เป็นอย่างไรบ้าง?"),
        (2, "📅 แจ้งเตือน: อย่าลืมนัดหมายของคุณ"),
        (3, "💬 คุณมีข้อความใหม่! โปรดตรวจสอบ"),
        (1, "🔐 แจ้งเตือนความปลอดภัย: มีการเข้าสู่ระบบจากอุปกรณ์ใหม่"),
    ]

    status_tasks = {user_id: asyncio.create_task(check_user_status_async(user_id)) for user_id in users}
    status_results = {user_id: await task for user_id, task in status_tasks.items()}

    pq = PriorityQueue()
    for priority, message in messages:
        pq.put((priority, message))

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        tasks = []
        while not pq.empty():
            _, message = pq.get()  # ดึงข้อความจากคิว
            for user_id in users:
                if status_results[user_id] == "online":  # ส่งข้อความเฉพาะผู้ใช้ที่ออนไลน์
                    tasks.append(loop.run_in_executor(executor, send_notification_in_thread, user_id, message))

        await asyncio.gather(*tasks)  

if __name__ == "__main__":
    start_time = time.time() 
    asyncio.run(main())  
    end_time = time.time() 
    print(f"⏳ ใช้เวลาทั้งหมด: {end_time - start_time:.2f} วินาที")