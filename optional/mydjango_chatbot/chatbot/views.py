import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dotenv import load_dotenv
import openai
from .models import ChatHistory

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


@login_required
def chatbot_view(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        # 시스템 역할을 DB에 저장 (필요에 따라 설정)
        system_prompt = "너는 친절한 선생님이야"

        # 사용자 메시지를 DB에 기록
        ChatHistory.objects.create(role="user", content=user_input, user=request.user)

        # 기존 대화 내역 불러오기
        conversation = ChatHistory.objects.filter(user=request.user).order_by(
            "timestamp"
        )

        # OpenAI chat messages 형식 생성
        messages = []
        # 시스템 역할 추가
        messages.append({"role": "system", "content": system_prompt})
        # Conversation DB 내용을 순서대로 추가
        for msg in conversation:
            # DB 상의 role과 OpenAI role 매핑
            openai_role = msg.role
            # content
            openai_content = msg.content
            messages.append({"role": openai_role, "content": openai_content})

        # OpenAI ChatCompletion 호출
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        ai_message = response["choices"][0]["message"]["content"]

        # 모델의 응답을 DB에 저장
        ChatHistory.objects.create(
            role="assistant", content=ai_message, user=request.user
        )

        return redirect("chatbot_page")
    else:
        # GET 요청 시 대화 내역 렌더링
        conversation = ChatHistory.objects.filter(user=request.user).order_by(
            "timestamp"
        )
        return render(
            request,
            "chatbot/chat_page.html",
            {"conversation": conversation, "username": request.user.username},
        )
