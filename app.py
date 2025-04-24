# --- ライブラリの読み込み ---
import streamlit as st
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# --- 環境変数の読み込み ---
load_dotenv()  # ローカル用（.envから読む）
openai_api_key = os.getenv("OPENAI_API_KEY")  # CloudではSecretsから読む

# --- ChatOpenAIのインスタンス作成 ---
chat = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.7,
    openai_api_key=openai_api_key  # ← これがないとCloudでエラー
)

# --- Streamlit UI設定 ---
st.set_page_config(page_title="LLM専門家アプリ", layout="centered")
st.title("🎓 LLMに専門家として回答してもらおう")
st.markdown("以下のフォームに質問を入力し、回答してほしい専門家の種類を選んでください。")

# --- 専門家の選択 ---
expert_type = st.radio("専門家の種類を選んでください：", ["歴史家", "心理カウンセラー", "プログラマー"])

# --- 質問入力フォーム ---
user_input = st.text_area("質問を入力してください")

# --- システムメッセージ生成関数 ---
def get_system_prompt(expert: str) -> str:
    prompts = {
        "歴史家": "あなたは優秀な歴史家です。以下の質問に歴史的背景や具体例を交えて答えてください。",
        "心理カウンセラー": "あなたは共感力に優れた心理カウンセラーです。感情に寄り添う優しい口調で回答してください。",
        "プログラマー": "あなたはプロのソフトウェアエンジニアです。正確な技術的情報を交えて回答してください。"
    }
    return prompts.get(expert, "あなたは親切なアシスタントです。")

# --- 回答生成関数 ---
def generate_response(question: str, expert: str) -> str:
    messages = [
        SystemMessage(content=get_system_prompt(expert)),
        HumanMessage(content=question)
    ]
    return chat(messages).content

# --- 実行ボタン ---
if st.button("実行"):
    if user_input.strip() == "":
        st.warning("質問を入力してください。")
    else:
        with st.spinner("LLMが考え中..."):
            response = generate_response(user_input, expert_type)
            st.success("✅ 回答が届きました！")
            st.write(response)
