import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

conversation_history = []

try:
    while True:
        content = input("무엇이든 물어보세요: ")

        if content.lower() == "exit":
            break

        # 사용자 메시지를 대화 기록에 추가
        conversation_history.append(f"User: {content}")

        # 대화형 모델을 사용하여 응답 생성
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "너는 친절한 선생님이야",
                },  # 프롬프트 명령
                {"role": "user", "content": content},  # 사용자 입력
            ],
        )
        generated_response = response.choices[0].message.content

        # 생성된 응답 출력
        print(generated_response)

        # 모델의 응답을 대화 기록에 추가
        conversation_history.append(f"Assistant: {generated_response}")

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    # 프로그램 종료 전에 대화 기록을 텍스트 파일로 저장
    with open("conversation_history.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(conversation_history))
    print("대화 내용이 'conversation_history.txt' 파일에 저장되었습니다.")
