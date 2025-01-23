import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

VALID_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june',
                'july', 'august', 'september', 'october', 'november', 'december']
VALID_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_user_input(prompt, valid_options):
    """사용자 입력을 받고 유효성을 검사."""
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print(f"잘못된 입력입니다. 다음 중에서 선택하세요: {valid_options}")

def get_filters():
    """사용자로부터 도시, 월, 요일 입력받기."""
    print('안녕하세요! 미국 자전거 공유 데이터를 탐색해봅시다!')

    city = get_user_input(f"분석할 도시를 선택하세요 {list(CITY_DATA.keys())}: ", CITY_DATA.keys())
    month = get_user_input("필터링할 월을 선택하세요 ('all', 'january' ... 'december'): ", VALID_MONTHS)
    day = get_user_input("필터링할 요일을 선택하세요 ('all', 'monday' ... 'sunday'): ", VALID_DAYS)

    print(f"\n입력한 값 - 도시: {city}, 월: {month}, 요일: {day}")
    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """도시 데이터 로드 및 필터링."""
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.strftime('%B').str.lower()
    df['Day'] = df['Start Time'].dt.day_name().str.lower()

    if month != 'all':
        df = df[df['Month'] == month]
    if day != 'all':
        df = df[df['Day'] == day]

    return df

def calculate_time_stats(df):
    """시간 통계 계산."""
    print('\n가장 빈번한 여행 시간 통계를 계산 중입니다...')
    start_time = time.time()

    common_month = df['Month'].mode()[0]
    common_day = df['Day'].mode()[0]
    common_hour = df['Start Time'].dt.hour.mode()[0]

    print(f"가장 흔한 월: {common_month}")
    print(f"가장 흔한 요일: {common_day}")
    print(f"가장 흔한 시간: {common_hour}시")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-' * 40)

def calculate_station_stats(df):
    """역 통계 계산."""
    print('\n가장 인기 있는 출발지와 도착지, 여행 경로 통계를 계산 중입니다...')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    frequent_trip = (df['Start Station'] + " -> " + df['End Station']).mode()[0]

    print(f"가장 많이 사용된 출발지: {common_start_station}")
    print(f"가장 많이 사용된 도착지: {common_end_station}")
    print(f"가장 빈번한 여행 경로: {frequent_trip}")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-' * 40)

def calculate_trip_duration_stats(df):
    """여행 시간 통계 계산."""
    print('\n여행 시간 통계를 계산 중입니다...')
    start_time = time.time()

    total_travel_time = df['Trip Duration'].sum()
    mean_travel_time = df['Trip Duration'].mean()

    print(f"총 여행 시간: {total_travel_time}초")
    print(f"평균 여행 시간: {mean_travel_time:.2f}초")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-' * 40)

def calculate_user_stats(df):
    """사용자 통계 계산."""
    print('\n사용자 통계를 계산 중입니다...')
    start_time = time.time()

    print("사용자 유형별 개수:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\n성별별 개수:")
        print(df['Gender'].value_counts())
    else:
        print("\n성별 데이터가 없습니다.")

    if 'Birth Year' in df.columns:
        print(f"\n가장 오래된 출생 연도: {int(df['Birth Year'].min())}")
        print(f"가장 최근 출생 연도: {int(df['Birth Year'].max())}")
        print(f"가장 흔한 출생 연도: {int(df['Birth Year'].mode()[0])}")
    else:
        print("출생 연도 데이터가 없습니다.")

    print(f"\n이 통계를 계산하는 데 {time.time() - start_time:.4f}초가 걸렸습니다.")
    print('-' * 40)

def display_raw_data(df):
    """원시 데이터를 5행씩 표시."""
    start_row = 0
    while True:
        show_data = input("\n원시 데이터를 5행씩 더 보시겠습니까? ('yes' 또는 'no'): ").lower()
        if show_data == 'yes':
            print(df.iloc[start_row:start_row + 5])
            start_row += 5
            if start_row >= len(df):
                print("\n더 이상 표시할 데이터가 없습니다.")
                break
        elif show_data == 'no':
            break
        else:
            print("잘못된 입력입니다. 'yes' 또는 'no'로 입력하세요.")

def main():
    """메인 프로그램 실행."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if df.empty:
            print("입력한 조건에 맞는 데이터가 없습니다.")
        else:
            display_raw_data(df)
            calculate_time_stats(df)
            calculate_station_stats(df)
            calculate_trip_duration_stats(df)
            calculate_user_stats(df)

        restart = input("\n다시 시작하시겠습니까? ('yes' 또는 'no'): ").lower()
        if restart != 'yes':
            print("프로그램을 종료합니다. 감사합니다!")
            break

if __name__ == "__main__":
    main()