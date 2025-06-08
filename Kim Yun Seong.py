from datetime import datetime, timedelta

# -------------------- 학생 정보 --------------------
student_ids = [str(25000 + i) for i in range(1, 129)]
student_id_name_map = {str(25000 + i): f"홍길동{i}" for i in range(1, 129)}

# -------------------- 기본 데이터 --------------------
teacher_schedule = {}
subject_queues = {}
subject_applied_students = {}
subject_recent_times = {}
student_time_registry = {}

# ✅ 추가: 모든 과목과 선생님 매핑
all_subjects = []
subject_teacher_map = {}


# -------------------- 유틸리티 --------------------
def get_avg_consult_time(subject):
    times = subject_recent_times.get(subject, [])
    return sum(times) // len(times) if times else 5


def is_teacher_available(subject, time_str):
    return time_str in teacher_schedule.get(subject, [])


def remove_student_from_queue(subject, student_id):
    queue = subject_queues.get(subject, [])
    for student in queue:
        if student["학생ID"] == student_id:
            queue.remove(student)
            break


def recommend_next_time(subject):
    available_times = teacher_schedule.get(subject, [])
    queue = subject_queues.get(subject, [])
    used_times = [student["신청시각"] for student in queue]
    for t in available_times:
        if t not in used_times:
            return t
    return "모든 시간대가 신청 완료됨"


def show_queue(subject):
    queue = subject_queues.get(subject, [])
    if not queue:
        print(f"[{subject}] 현재 대기 중인 학생이 없습니다.")
    else:
        print(f"[{subject}] 현재 대기열:")
        for idx, student in enumerate(queue, 1):
            print(
                f"{idx}. {student['이름']}({student['학생ID']}) - {student['신청시각']} | 예상 {student['평균상담시간']}분"
            )


def parse_time_range(time_range_str):
    try:
        start_str, end_str = time_range_str.split("~")
        start_time = datetime.strptime(start_str.strip(), "%H:%M")
        end_time = datetime.strptime(end_str.strip(), "%H:%M")
        time_list = []
        while start_time < end_time:
            time_list.append(start_time.strftime("%H:%M"))
            start_time += timedelta(minutes=10)
        return time_list
    except:
        print("[에러] 시간 형식이 잘못되었습니다. 예: 12:00~14:00")
        return []


# -------------------- 선생님 등록 --------------------
def register_teacher():
    name = input("선생님 이름 입력: ").strip()
    subject = input("과목 입력: ").strip()
    raw_ranges = (
        input("가능 시간 입력 (여러 범위를 ,로 구분, 예: 12:00~13:00,14:00~15:00): ")
        .strip()
        .split(",")
    )

    all_times = []
    for r in raw_ranges:
        all_times.extend(parse_time_range(r.strip()))
    if not all_times:
        return

    teacher_schedule[subject] = all_times
    subject_queues.setdefault(subject, [])
    subject_applied_students.setdefault(subject, set())
    subject_recent_times.setdefault(subject, [])

    # ✅ 과목 등록 및 선생님 매핑
    if subject not in all_subjects:
        all_subjects.append(subject)
    subject_teacher_map[subject] = name

    print(
        f"[등록 완료] {name} 선생님의 '{subject}' 과목 상담 가능 시간: {teacher_schedule[subject]}"
    )


# -------------------- 학생 신청 --------------------
def register_student():
    student_id = input("학번(ID) 입력: ").strip()
    if student_id not in student_ids:
        print("[에러] 잘못된 학번 입력입니다.")
        return
    student_name = input("이름 입력: ").strip()
    if student_id_name_map.get(student_id) != student_name:
        print("[에러] 학번과 이름이 일치하지 않습니다.")
        return
    subject = input("이의제기 과목 입력: ").strip()
    if subject not in all_subjects:
        print("[에러] 잘못된 과목 입력입니다.")
        return
    teacher_name = input("담당 선생님 이름 입력: ").strip()
    if subject_teacher_map.get(subject) != teacher_name:
        print("[에러] 과목과 담당 선생님 정보가 일치하지 않습니다.")
        return
    request_time = input("이의제기 시간 (HH:MM 형식): ").strip()

    if not is_teacher_available(subject, request_time):
        print(f"[불가] {subject} 과목은 {request_time}에 상담이 불가능합니다.")
        return
    if student_id in subject_applied_students[subject]:
        print(f"[중복 신청] {student_name}({student_id})은 이미 신청했습니다.")
        return
    if (
        student_id in student_time_registry
        and request_time in student_time_registry[student_id]
    ):
        print(
            f"[시간 중복] {student_name}({student_id})은 이미 {request_time}에 신청했습니다."
        )
        return

    avg_time = get_avg_consult_time(subject)
    subject_queues[subject].append(
        {
            "학생ID": student_id,
            "이름": student_name,
            "신청시각": request_time,
            "평균상담시간": avg_time,
        }
    )
    subject_applied_students[subject].add(student_id)
    student_time_registry.setdefault(student_id, []).append(request_time)

    print(
        f"[신청 완료] {student_name}({student_id}) → {subject} {request_time} 신청. 예상 상담시간: {avg_time}분"
    )


# -------------------- 상담 기록/대기열/추천 --------------------
def record_consult_time():
    subject = input("상담 과목 입력: ").strip()
    student_id = input("상담한 학생의 학번(ID) 입력: ").strip()
    minutes = input("상담에 걸린 시간 (분): ").strip()
    if not minutes.isdigit():
        print("[에러] 숫자로 입력해야 합니다.")
        return
    minutes = int(minutes)
    subject_recent_times.setdefault(subject, []).append(minutes)
    if len(subject_recent_times[subject]) > 5:
        subject_recent_times[subject] = subject_recent_times[subject][-5:]
    remove_student_from_queue(subject, student_id)
    print(
        f"[기록 완료] {student_id} 학생의 상담 시간 {minutes}분이 '{subject}' 과목에 기록되었습니다."
    )


def view_queue():
    subject = input("조회할 과목 입력: ").strip()
    if subject in teacher_schedule:
        show_queue(subject)
    else:
        print(f"[에러] {subject} 과목은 아직 등록되지 않았습니다.")


# -------------------- 실행 루프 --------------------
def run_system():
    while True:
        role = input("\n[학생/선생님/기록/대기열/종료] 중 하나를 입력하세요: ").strip()
        if role == "학생":
            register_student()
        elif role == "선생님":
            register_teacher()
        elif role == "기록":
            record_consult_time()
        elif role == "대기열":
            view_queue()
        elif role == "종료":
            print("시스템을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")


# -------------------- 메인 실행 --------------------
if __name__ == "__main__":
    run_system()
