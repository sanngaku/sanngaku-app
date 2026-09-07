from collections import Counter
import itertools
import os
import random

import altair as alt
from PIL import Image
import pandas as pd
import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        password = st.text_input("パスワードを入力してください", type="password")
        if st.button("ログイン"):
            if password == "sanngaku913117":  # ← ここを好きなパスワードに変更
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("パスワードが違います")
        return False
    return True

# --- 修正後 ---
ICON_PATH_1 = "アイコン/1.png"
ICON_PATH_2 = "アイコン/2.png"

# アプリの基本設定
if os.path.exists(ICON_PATH_1):
    app_icon = Image.open(ICON_PATH_1)
else:
    app_icon = "⛰️"

st.set_page_config(
    page_title="山岳部 班決め・共同装備振り分け",
    page_icon=app_icon,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap');

    :root {
        --primary-color: #485736 !important;
    }

    html, body, [data-testid="stAppViewContainer"], .stApp {
        font-family: 'Zen Kaku Gothic New', 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F4F1E9 !important;
        color: #000000 !important;
    }

    [data-testid="stHeader"] {
        background-color: #F4F1E9 !important;
    }

    h1, [data-testid="stMarkdownContainer"] h1 {
        color: #485736 !important;
        font-weight: 700 !important;
    }

    h2, h3, h4, h5, h6, 
    [data-testid="stMarkdownContainer"] h2, 
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    p, span, label, div,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    .stSelectbox label,
    .stNumberInput label {
        color: #000000 !important;
    }

    /* サイドバーの背景色と固定スタイル */
    [data-testid="stSidebar"] {
        background-color: #DBC79C !important;
        border-right: 1px solid #C4B28B !important;
    }
    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 6px !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        background-color: transparent !important;
        color: #000000 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        display: flex !important;
        align-items: center !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(72, 87, 54, 0.1) !important;
    }
    [data-testid="stSidebar"] .stRadio input:checked + div {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background-color: #485736 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input:checked) * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* ボタンの共通スタイリング */
    button[kind="primary"], 
    button[kind="secondary"],
    .stButton > button,
    [data-testid="baseButton-primary"],
    [data-testid="baseButton-secondary"] {
        background-color: #485736 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    .stButton > button * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .stButton > button:hover {
        background-color: #38432A !important;
        color: #FFFFFF !important;
    }

    /* 表（データフレーム・テーブル） */
    [data-testid="stDataFrame"], 
    [data-testid="stTable"],
    div[data-testid="stDataFrame"] > div,
    iframe[title="streamlit.dataframe"] {
        border-radius: 10px !important;
        border: 1px solid #D0DAD0 !important;
    }

    /* トグル・チェックボックスの強制色設定 */
    [data-testid="stCheckbox"], 
    [data-testid="stToggle"],
    .stToggle {
        background-color: #485736 !important;
        padding: 10px 18px !important;
        border-radius: 20px !important;
        border: 2px solid #38432A !important;
        display: inline-flex !important;
        align-items: center !important;
    }
    [data-testid="stCheckbox"] *, 
    [data-testid="stToggle"] *,
    .stToggle * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* タブの美観と動作 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        border-bottom: 2px solid #D0DAD0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #E9E4D2 !important;
        border-radius: 8px 8px 0px 0px !important;
        padding: 10px 20px !important;
        color: #000000 !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #485736 !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] * {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .belongings-box {
        background-color: #EEF0F4 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin-top: 4px !important;
        color: #000000 !important;
        font-size: 1rem !important;
    }

    .stAlert {
        background-color: #E9E4D2 !important;
        color: #000000 !important;
        border: 1px solid #D0DAD0 !important;
        border-radius: 8px !important;
    }

    /* ダークモード時のドロップダウン/プルダウン文字色白・背景黒設定 */
    @media (prefers-color-scheme: dark) {
        div[data-baseweb="select"], 
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"],
        ul[role="listbox"],
        li[role="option"] {
            background-color: #1E1E1E !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] div,
        div[data-baseweb="select"] input,
        div[data-baseweb="select"] svg,
        ul[role="listbox"] li,
        li[role="option"] div,
        li[role="option"] span {
            color: #FFFFFF !important;
        }

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            background-color: #333333 !important;
            color: #FFFFFF !important;
        }
    }
    </style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def connect_to_gsheet():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    import json
    import os
    import gspread
    from google.oauth2.service_account import Credentials

    # Renderの環境変数を優先的に読み込み、無ければローカルファイルを読む
    if "CREDENTIALS_JSON" in os.environ:
        creds_dict = json.loads(os.environ["CREDENTIALS_JSON"])
        creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    else:
        json_path = "credentials.json"
        creds = Credentials.from_service_account_file(json_path, scopes=scopes)

    client = gspread.authorize(creds)
    return client.open("山岳部")


try:
    spreadsheet = connect_to_gsheet()
except Exception as e:
    st.error(f"スプレッドシート接続エラー: {e}")
    st.stop()


@st.cache_data(ttl=60)
def load_sheet_data(sheet_name):
    ws = spreadsheet.worksheet(sheet_name)
    return pd.DataFrame(ws.get_all_records())


def serialize_list_col(val):
    if isinstance(val, list):
        return ", ".join(str(x) for x in val)
    return str(val) if pd.notna(val) else ""


def deserialize_list_col(val):
    if isinstance(val, list):
        return val
    if pd.notna(val) and str(val).strip() != "":
        return [item.strip() for item in str(val).split(",") if item.strip()]
    return []


def update_sheet_safely(sheet_name, df):
    ws = spreadsheet.worksheet(sheet_name)
    ws.clear()
    clean_df = df.astype(str)
    ws.update([clean_df.columns.values.tolist()] + clean_df.values.tolist())


def sort_by_hrno(df):
    """HRNO（数値昇順）順に正確にソート"""
    if "HRNO" in df.columns:
        df["_hrno_temp"] = (
            pd.to_numeric(df["HRNO"], errors="coerce").fillna(9999).astype(int)
        )
        df = df.sort_values(by="_hrno_temp", ascending=True).drop(
            columns=["_hrno_temp"]
        )
    return df


def ensure_required_columns(df):
    required_cols = {
        "HRNO": "9999",
        "名前": "",
        "性別": "男",
        "学年": 1,
        "行動班": "",
        "食事班": "",
        "テント班": "",
        "共同装備": [],
        "重量": 0,
        "係": [],
    }
    for col, default_val in required_cols.items():
        if col not in df.columns:
            if isinstance(default_val, list):
                df[col] = [[] for _ in range(len(df))]
            else:
                df[col] = default_val
    return df


# --- サイドバー表示 ---
with st.sidebar:
    c1, c2 = st.columns([1, 2])
    if os.path.exists(ICON_PATH_1):
        c1.image(Image.open(ICON_PATH_1), use_container_width=True)
    if os.path.exists(ICON_PATH_2):
        c2.image(Image.open(ICON_PATH_2), use_container_width=True)

    st.markdown(
        "<span style='font-size: 1.1rem; font-weight: bold; color: #000000; display: inline-block; margin-top: 5px; margin-bottom: 10px;'>班決め・共同装備振り分け</span>",
        unsafe_allow_html=True,
    )

page = st.sidebar.radio(
    "",
    [
        "トップ",
        "名簿・設定",
        "班決め・共同装備振り分け",
        "計画書出力",
    ],
    label_visibility="collapsed",
)

if page == "トップ":
    st.markdown(
        "<h1>山岳部 班決め・共同装備振り分け</h1>",
        unsafe_allow_html=True,
    )
    st.info("スプレッドシートとリアルタイム連携された自動化アプリです。")

elif page == "名簿・設定":
    st.markdown(
        "<h1>名簿・設定</h1>",
        unsafe_allow_html=True,
    )

    mode = st.toggle("編集モードを有効にする", value=False)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "名簿（生徒）",
        "名簿（先生・OB/OG）",
        "テント設定",
        "班設定",
        "共同装備設定",
    ])

    with tab1:
        st.subheader("生徒名簿一覧")
        df_student = load_sheet_data("名簿（生徒）")

        if "HRNO" in df_student.columns:
            df_student["HRNO"] = df_student["HRNO"].astype(str).str.zfill(4)
        if "学年" in df_student.columns:
            df_student["学年"] = (
                pd.to_numeric(df_student["学年"], errors="coerce")
                .fillna(1)
                .astype(int)
            )
        if "参加" in df_student.columns:
            df_student["参加"] = df_student["参加"].isin(
                [True, 1, "TRUE", "true", "True"]
            )
        if "係" in df_student.columns:
            df_student["係"] = df_student["係"].apply(deserialize_list_col)

        if mode:
            student_config = {
                "HRNO": st.column_config.TextColumn(
                    "HRNO", help="半角4桁の数字", max_chars=4
                ),
                "名前": st.column_config.TextColumn("名前"),
                "学年": st.column_config.NumberColumn(
                    "学年", min_value=1, max_value=3, step=1
                ),
                "性別": st.column_config.SelectboxColumn(
                    "性別", options=["男", "女"], required=True
                ),
                "係": st.column_config.MultiselectColumn(
                    "係",
                    options=[
                        "装備係",
                        "食事係",
                        "天気図係",
                        "記録係",
                        "医療係",
                    ],
                ),
                "参加": st.column_config.CheckboxColumn("参加", default=True),
            }
            edited_student = st.data_editor(
                df_student,
                column_config=student_config,
                num_rows="dynamic",
                key="editor_student",
                use_container_width=True,
            )
            if st.button("生徒名簿を保存"):
                df_to_save = edited_student.copy()
                if "係" in df_to_save.columns:
                    df_to_save["係"] = df_to_save["係"].apply(serialize_list_col)
                df_to_save = df_to_save.fillna("")
                update_sheet_safely("名簿（生徒）", df_to_save)
                st.cache_data.clear()
                st.toast("生徒名簿を保存しました。")
        else:
            df_display = df_student.copy()
            if "係" in df_display.columns:
                df_display["係"] = df_display["係"].apply(serialize_list_col)
            st.dataframe(df_display, use_container_width=True)

    with tab2:
        st.subheader("先生・OB/OG名簿一覧")
        df_adult = load_sheet_data("名簿（先生・OB/OG）")
        if "参加" in df_adult.columns:
            df_adult["参加"] = df_adult["参加"].isin(
                [True, 1, "TRUE", "true", "True"]
            )

        if mode:
            adult_config = {
                "名前": st.column_config.TextColumn("名前"),
                "区分": st.column_config.SelectboxColumn(
                    "区分", options=["先生", "OB", "OG"], required=True
                ),
                "性別": st.column_config.SelectboxColumn(
                    "性別", options=["男", "女"], required=True
                ),
                "参加": st.column_config.CheckboxColumn("参加", default=True),
            }
            edited_adult = st.data_editor(
                df_adult,
                column_config=adult_config,
                num_rows="dynamic",
                key="editor_adult",
                use_container_width=True,
            )
            if st.button("先生・OB/OG名簿を保存"):
                df_to_save = edited_adult.fillna("")
                update_sheet_safely("名簿（先生・OB/OG）", df_to_save)
                st.cache_data.clear()
                st.toast("大人名簿を保存しました。")
        else:
            st.dataframe(df_adult, use_container_width=True)

    with tab3:
        st.subheader("生徒用テント")
        df_tent_student = load_sheet_data("テント（生徒）")

        tent_config = {
            "テント名": st.column_config.TextColumn("テント名"),
            "定員": st.column_config.NumberColumn(
                "定員", min_value=1, step=1
            ),
            "優先度": st.column_config.NumberColumn(
                "優先度", min_value=1, step=1
            ),
            "状態": st.column_config.SelectboxColumn(
                "状態",
                options=[
                    "利用可能",
                    "本体不備",
                    "フライ不備",
                    "ポール不備",
                    "ペグ不備",
                    "修理中",
                ],
                required=True,
            ),
        }

        if mode:
            edited_tent_student = st.data_editor(
                df_tent_student,
                column_config=tent_config,
                num_rows="dynamic",
                key="editor_tent_s",
                use_container_width=True,
            )
        else:
            st.dataframe(df_tent_student, use_container_width=True)

        st.subheader("先生・OB/OG用テント")
        df_tent_adult = load_sheet_data("テント（先生・OB/OG）")

        if mode:
            edited_tent_adult = st.data_editor(
                df_tent_adult,
                column_config=tent_config,
                num_rows="dynamic",
                key="editor_tent_a",
                use_container_width=True,
            )
            if st.button("テント設定をすべて保存"):
                df_s_save = edited_tent_student.fillna("")
                update_sheet_safely("テント（生徒）", df_s_save)

                df_a_save = edited_tent_adult.fillna("")
                update_sheet_safely("テント（先生・OB/OG）", df_a_save)

                st.cache_data.clear()
                st.toast("テント設定を保存しました。")
        else:
            st.dataframe(df_tent_adult, use_container_width=True)

    with tab4:
        st.subheader("班数・条件設定")
        try:
            df_group_set = load_sheet_data("班設定")
            act_num = (
                int(
                    df_group_set[df_group_set["項目"] == "行動班数"][
                        "設定値"
                    ].values[0]
                )
                if "行動班数" in df_group_set["項目"].values
                else 2
            )
            meal_num = (
                int(
                    df_group_set[df_group_set["項目"] == "食事班数"][
                        "設定値"
                    ].values[0]
                )
                if "食事班数" in df_group_set["項目"].values
                else 3
            )
        except Exception:
            act_num, meal_num = 2, 3

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 行動班設定")
            new_act_num = st.selectbox(
                "行動班の数",
                options=[1, 2, 3],
                index=[1, 2, 3].index(act_num) if act_num in [1, 2, 3] else 1,
            )

        with col2:
            st.markdown("### 食事班設定")
            meal_options_list = [1, 2, 3, 4, 5, 6, 7]
            new_meal_num = st.selectbox(
                "食事班の数",
                options=meal_options_list,
                index=meal_options_list.index(meal_num)
                if meal_num in meal_options_list
                else 2,
            )

        st.markdown("---")
        st.markdown("### テント班設定")
        st.info(
            "※「テント設定」タブを参照します。優先度の合計が男女で平準化されるよう最適割り当てします。"
        )

        if st.button("班設定を保存"):
            df_save = pd.DataFrame([
                {"項目": "行動班数", "設定値": new_act_num},
                {"項目": "食事班数", "設定値": new_meal_num},
            ])
            update_sheet_safely("班設定", df_save)
            st.cache_data.clear()
            st.toast("班設定を保存しました。")

    with tab5:
        st.subheader("共同装備設定一覧")
        df_gear = load_sheet_data("共同装備")

        if "数" in df_gear.columns:
            df_gear["数"] = df_gear["数"].astype(str)

        if mode:
            gear_config = {
                "種類": st.column_config.SelectboxColumn(
                    "種類", options=["テント", "食事", "その他"], required=True
                ),
                "装備名": st.column_config.TextColumn("装備名"),
                "重量": st.column_config.NumberColumn(
                    "重量", min_value=1, max_value=10, step=1
                ),
                "数": st.column_config.SelectboxColumn(
                    "数",
                    options=[
                        "テント班数",
                        "食事班数",
                        "行動班数",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                    ],
                    required=True,
                ),
                "条件": st.column_config.SelectboxColumn(
                    "条件",
                    options=[
                        "テント班対応",
                        "食事班対応",
                        "行動班対応",
                        "装備係",
                        "食事係",
                        "天気図係",
                        "記録係",
                        "医療係",
                        "フリー",
                    ],
                    required=True,
                ),
            }
            edited_gear = st.data_editor(
                df_gear,
                column_config=gear_config,
                num_rows="dynamic",
                key="editor_gear",
                use_container_width=True,
            )
            if st.button("共同装備設定を保存"):
                df_to_save = edited_gear.fillna("")
                update_sheet_safely("共同装備", df_to_save)
                st.cache_data.clear()
                st.toast("共同装備設定を保存しました。")
        else:
            st.dataframe(df_gear, use_container_width=True)

elif page == "班決め・共同装備振り分け":
    st.markdown(
        "<h1>班決め・共同装備振り分け</h1>",
        unsafe_allow_html=True,
    )

    ACT_MARU = ["❶", "❷", "❸"]
    MEAL_MARU = ["①", "②", "③", "④", "⑤", "⑥", "⑦"]

    def run_auto_grouping():
        """1段階目：自動班決め"""
        df_students = load_sheet_data("名簿（生徒）")
        df_students = df_students[
            df_students["参加"].isin([True, 1, "TRUE", "true", "True"])
        ].copy()

        df_adults = load_sheet_data("名簿（先生・OB/OG）")
        df_adults = df_adults[
            df_adults["参加"].isin([True, 1, "TRUE", "true", "True"])
        ].copy()

        try:
            df_group_set = load_sheet_data("班設定")
            act_cnt = int(
                df_group_set[df_group_set["項目"] == "行動班数"]["設定値"].values[0]
            )
            meal_cnt = int(
                df_group_set[df_group_set["項目"] == "食事班数"]["設定値"].values[0]
            )
        except Exception:
            act_cnt, meal_cnt = 2, 3

        act_labels = ACT_MARU[:act_cnt]
        meal_labels = MEAL_MARU[:meal_cnt]

        students_list = df_students.to_dict("records")
        for s in students_list:
            s["is_adult"] = False
            s["係_list"] = deserialize_list_col(s.get("係", []))

        adults_list = df_adults.to_dict("records")
        for a in adults_list:
            a["is_adult"] = True
            a["HRNO"] = "9999"
            a["学年"] = 0
            a["係_list"] = []

        all_members = students_list + adults_list

        def allocate_balanced_strict(members, labels, is_act=True):
            groups = {l: [] for l in labels}
            assigned = []

            if is_act:
                for m in members:
                    if "難波" in str(m.get("名前", "")):
                        groups[labels[0]].append(m)
                        assigned.append(m)

            remaining = [m for m in members if m not in assigned]
            adults_rem = [m for m in remaining if m.get("is_adult")]
            students_rem = [m for m in remaining if not m.get("is_adult")]
            random.shuffle(adults_rem)

            for m in adults_rem:
                min_len = min(len(groups[l]) for l in labels)
                candidate_labels = [l for l in labels if len(groups[l]) == min_len]
                target_label = random.choice(candidate_labels)
                groups[target_label].append(m)

            def get_attr_key(m):
                if is_act:
                    return (m.get("性別"), m.get("学年"))
                else:
                    return (
                        "食事係" in m.get("係_list", []),
                        m.get("性別"),
                        m.get("学年"),
                    )

            attr_buckets = {}
            for m in students_rem:
                key = get_attr_key(m)
                attr_buckets.setdefault(key, []).append(m)

            for key, bucket in attr_buckets.items():
                random.shuffle(bucket)
                for m in bucket:
                    min_len = min(len(groups[l]) for l in labels)
                    candidate_labels = [l for l in labels if len(groups[l]) == min_len]
                    target_label = random.choice(candidate_labels)
                    groups[target_label].append(m)

            for l, g_list in groups.items():
                for m in g_list:
                    if is_act:
                        m["行動班"] = l
                    else:
                        m["食事班"] = l

        allocate_balanced_strict(all_members, act_labels, is_act=True)
        allocate_balanced_strict(all_members, meal_labels, is_act=False)

        # テント班設定（生徒のみ対象）
        df_tents = load_sheet_data("テント（生徒）")
        df_tents_avail = df_tents[df_tents["状態"] == "利用可能"].copy()
        df_tents_avail["優先度"] = (
            pd.to_numeric(df_tents_avail["優先度"], errors="coerce").fillna(999)
        )
        df_tents_avail["定員"] = (
            pd.to_numeric(df_tents_avail["定員"], errors="coerce").fillna(0)
        )
        df_tents_avail = df_tents_avail.sort_values(
            by="優先度", ascending=True
        ).reset_index(drop=True)

        males = [s for s in students_list if s.get("性別") == "男"]
        females = [s for s in students_list if s.get("性別") == "女"]

        def calculate_required_tents(group_size, available_tents):
            rem = group_size
            assigned_plan = []
            for _, tent in available_tents.iterrows():
                if rem <= 0:
                    break
                cap = int(tent["定員"])
                if cap <= 0:
                    continue
                num = cap if rem >= cap else (cap - 1 if rem == cap - 1 else rem)
                assigned_plan.append((tent, num))
                rem -= num
            return assigned_plan

        def sort_by_grade_balance(group_students):
            g1 = [s for s in group_students if s.get("学年") == 1]
            g2 = [s for s in group_students if s.get("学年") == 2]
            g3 = [s for s in group_students if s.get("学年") == 3]
            random.shuffle(g1)
            random.shuffle(g2)
            random.shuffle(g3)
            balanced = []
            max_len = max(len(g1), len(g2), len(g3)) if (g1 or g2 or g3) else 0
            for i in range(max_len):
                if i < len(g3):
                    balanced.append(g3[i])
                if i < len(g2):
                    balanced.append(g2[i])
                if i < len(g1):
                    balanced.append(g1[i])
            return balanced

        needed_tents_plan = calculate_required_tents(
            len(students_list), df_tents_avail
        )
        num_male_tents = len(
            calculate_required_tents(len(males), df_tents_avail)
        )
        all_tent_indices = list(range(len(needed_tents_plan)))
        best_diff, best_male_indices = float("inf"), []

        for male_comb in itertools.combinations(
            all_tent_indices, num_male_tents
        ):
            female_comb = [i for i in all_tent_indices if i not in male_comb]
            sum_m = sum(needed_tents_plan[i][0]["優先度"] for i in male_comb)
            sum_f = sum(needed_tents_plan[i][0]["優先度"] for i in female_comb)
            if abs(sum_m - sum_f) < best_diff:
                best_diff = abs(sum_m - sum_f)
                best_male_indices = list(male_comb)

        male_tent_plans = [needed_tents_plan[i] for i in best_male_indices]
        female_tent_plans = [
            needed_tents_plan[i]
            for i in all_tent_indices
            if i not in best_male_indices
        ]

        def apply_tent_assignment(group_students, tent_plans):
            balanced = sort_by_grade_balance(group_students)
            st_idx = 0
            for tent_info, num_people in tent_plans:
                t_name = str(tent_info["テント名"])
                for _ in range(num_people):
                    if st_idx < len(balanced):
                        balanced[st_idx]["テント班"] = t_name
                        st_idx += 1

        apply_tent_assignment(males, male_tent_plans)
        apply_tent_assignment(females, female_tent_plans)

        res_df = pd.DataFrame(all_members)
        res_df = ensure_required_columns(res_df)
        res_df = sort_by_hrno(res_df)
        return res_df

    def get_gear_item_pool(current_df):
        """共同装備設定に基づきアイテムプールを作成"""
        df_gears = load_sheet_data("共同装備")
        students_list = current_df.to_dict("records")

        all_used_tents = list(
            set([s.get("テント班") for s in students_list if s.get("テント班")])
        )
        meal_labels = list(
            set([s.get("食事班") for s in students_list if s.get("食事班")])
        )
        act_labels = list(
            set([s.get("行動班") for s in students_list if s.get("行動班")])
        )

        item_pool = []
        for _, g in df_gears.iterrows():
            g_type = str(g.get("種類", "その他"))
            g_name = str(g["装備名"])
            g_weight = int(g["重量"]) if str(g["重量"]).isdigit() else 1
            g_num_str = str(g["数"])
            g_cond = str(g["条件"])

            if g_cond == "テント班対応":
                for t in all_used_tents:
                    item_pool.append({
                        "full_name": f"{t}：{g_name}",
                        "weight": g_weight,
                        "target_type": "テント班",
                        "target_val": t,
                        "type": g_type,
                        "raw_name": g_name,
                    })
            elif g_cond == "食事班対応":
                for m in meal_labels:
                    item_pool.append({
                        "full_name": f"{m}：{g_name}",
                        "weight": g_weight,
                        "target_type": "食事班",
                        "target_val": m,
                        "type": g_type,
                        "raw_name": g_name,
                    })
            elif g_cond == "行動班対応":
                for a in act_labels:
                    item_pool.append({
                        "full_name": f"{a}：{g_name}",
                        "weight": g_weight,
                        "target_type": "行動班",
                        "target_val": a,
                        "type": g_type,
                        "raw_name": g_name,
                    })
            elif "係" in g_cond:
                item_pool.append({
                    "full_name": g_name,
                    "weight": g_weight,
                    "target_type": "係",
                    "target_val": g_cond,
                    "type": g_type,
                    "raw_name": g_name,
                })
            else:
                cnt = int(g_num_str) if g_num_str.isdigit() else 1
                for _ in range(cnt):
                    item_pool.append({
                        "full_name": g_name,
                        "weight": g_weight,
                        "target_type": "フリー",
                        "target_val": "全員",
                        "type": g_type,
                        "raw_name": g_name,
                    })

        item_pool.sort(key=lambda x: x["weight"], reverse=True)
        return item_pool

    def run_auto_gear_assignment(current_df):
        """2段階目：自動共同装備振り分け（生徒のみを対象）"""
        all_list = current_df.to_dict("records")
        for s in all_list:
            s["係_list"] = deserialize_list_col(s.get("係", []))
            s["共同装備"] = []
            s["重量"] = 0

        students_list = [s for s in all_list if str(s.get("HRNO", "")) != "9999"]
        item_pool = get_gear_item_pool(current_df)

        for item in item_pool:
            ttype, tval = item["target_type"], item["target_val"]
            if ttype == "テント班":
                candidates = [
                    s for s in students_list if s.get("テント班") == tval
                ]
            elif ttype == "食事班":
                candidates = [
                    s for s in students_list if s.get("食事班") == tval
                ]
            elif ttype == "行動班":
                candidates = [
                    s for s in students_list if s.get("行動班") == tval
                ]
            elif ttype == "係":
                candidates = [
                    s for s in students_list if tval in s["係_list"]
                ]
            else:
                candidates = students_list

            if candidates:
                candidates.sort(key=lambda x: (x["重量"], random.random()))
                selected_student = candidates[0]
                selected_student["共同装備"].append(item["full_name"])
                selected_student["重量"] += item["weight"]

        res_df = pd.DataFrame(all_list)
        res_df = ensure_required_columns(res_df)
        res_df = sort_by_hrno(res_df)
        return res_df, item_pool

    def save_p3_to_gsheet(df_to_save, target="all"):
        save_df = df_to_save.copy()
        if "共同装備" in save_df.columns:
            save_df["共同装備"] = save_df["共同装備"].apply(serialize_list_col)
        if "係" in save_df.columns:
            save_df["係"] = save_df["係"].apply(serialize_list_col)
        if "係_list" in save_df.columns:
            save_df = save_df.drop(columns=["係_list"])
        if "is_adult" in save_df.columns:
            save_df = save_df.drop(columns=["is_adult"])

        save_df = save_df.fillna("")
        update_sheet_safely("名簿（生徒）", save_df)
        st.cache_data.clear()

        msg = {
            "all": "全班および装備の変更内容を保存しました。",
            "act": "行動班の設定を保存しました。",
            "meal": "食事班の設定を保存しました。",
            "tent": "テント班の設定を保存しました。",
            "gear": "共同装備の設定を保存しました。",
        }.get(target, "保存しました。")
        st.toast(msg)

    edit_mode_p3 = st.toggle("編集モードを有効にする", value=False)

    # 初回読み込み時の初期データセット
    if "p3_data" not in st.session_state:
        df_students_init = load_sheet_data("名簿（生徒）")
        df_students_init = ensure_required_columns(df_students_init)
        df_students_init = sort_by_hrno(df_students_init)
        if "共同装備" in df_students_init.columns:
            df_students_init["共同装備"] = df_students_init["共同装備"].apply(
                deserialize_list_col
            )
        st.session_state["p3_data"] = df_students_init
        st.session_state["p3_item_pool"] = []

    df_p3 = ensure_required_columns(st.session_state["p3_data"])
    df_p3 = sort_by_hrno(df_p3)
    item_pool = st.session_state.get("p3_item_pool", [])
    if not item_pool:
        item_pool = get_gear_item_pool(df_p3)

    try:
        df_group_set = load_sheet_data("班設定")
        act_cnt = int(
            df_group_set[df_group_set["項目"] == "行動班数"]["設定値"].values[0]
        )
        meal_cnt = int(
            df_group_set[df_group_set["項目"] == "食事班数"]["設定値"].values[0]
        )
    except Exception:
        act_cnt, meal_cnt = 2, 3

    act_options = [""] + ACT_MARU[:act_cnt]
    meal_options = [""] + MEAL_MARU[:meal_cnt]

    try:
        df_tents_s = load_sheet_data("テント（生徒）")
        df_tents_a = load_sheet_data("テント（先生・OB/OG）")
        avail_s = df_tents_s[df_tents_s["状態"] == "利用可能"]["テント名"].tolist()
        avail_a = df_tents_a[df_tents_a["状態"] == "利用可能"]["テント名"].tolist()
        tent_options = [""] + sorted(list(set(avail_s + avail_a)))
    except Exception:
        tent_options = [""] + list(df_p3["テント班"].dropna().unique())

    # 水平線(---)を消去し余白をカット

    tab_list = ["一覧表", "行動班詳細", "食事班詳細", "テント班詳細", "共同装備詳細"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(tab_list)

    with tab1:
        st.subheader("一覧表")

        if edit_mode_p3:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("① 自動班決め実行", key="p3_run_grouping"):
                    df_res = run_auto_grouping()
                    st.session_state["p3_data"] = df_res
                    st.toast("行動班・食事班・テント班の自動振り分けを完了しました。")
                    st.rerun()

            with col_btn2:
                if st.button(
                    "② 自動共同装備振り分け実行", key="p3_run_gear"
                ):
                    df_res, pool = run_auto_gear_assignment(df_p3)
                    st.session_state["p3_data"] = df_res
                    st.session_state["p3_item_pool"] = pool
                    st.toast("共同装備の自動振り分けを完了しました。")
                    st.rerun()

        df_table = df_p3.copy()
        df_table["共同装備"] = df_table["共同装備"].apply(serialize_list_col)

        target_columns = ["名前", "行動班", "食事班", "テント班", "共同装備", "重量"]
        show_df = df_table[
            [c for c in target_columns if c in df_table.columns]
        ]

        list_column_config = {
            "名前": st.column_config.TextColumn("名前", width="small"),
            "行動班": st.column_config.TextColumn("行動班", width="small"),
            "食事班": st.column_config.TextColumn("食事班", width="small"),
            "テント班": st.column_config.TextColumn("テント班", width="small"),
            "共同装備": st.column_config.TextColumn("共同装備", width="large"),
            "重量": st.column_config.NumberColumn("重量", width="small"),
        }

        st.dataframe(
            show_df,
            column_config=list_column_config,
            use_container_width=True,
            hide_index=True,
        )

        if edit_mode_p3:
            st.markdown("---")
            if st.button("全体を保存（班・装備すべて）", key="save_all"):
                save_p3_to_gsheet(df_p3, target="all")

    with tab2:
        st.subheader("行動班詳細")
        act_groups = sorted([g for g in df_p3["行動班"].unique() if str(g).strip() != ""])

        if not act_groups:
            st.info("まだ行動班が割り当てられていません。「① 自動班決め実行」ボタンを押してください。")
        else:
            if edit_mode_p3:
                st.info("各生徒の行動班を変更できます。")
                has_act_changed = False
                for idx, row in df_p3.iterrows():
                    col_name, col_sel = st.columns([1, 2])
                    with col_name:
                        st.write(
                            f"**{row['名前']}** ({row.get('性別','')}/{row.get('学年','')}年)"
                        )
                    with col_sel:
                        curr_act = str(row.get("行動班", ""))
                        new_act = st.selectbox(
                            f"{row['名前']} の行動班",
                            options=act_options,
                            index=act_options.index(curr_act)
                            if curr_act in act_options
                            else 0,
                            key=f"act_sel_{idx}_{curr_act}",
                            label_visibility="collapsed",
                        )
                        if new_act != curr_act:
                            df_p3.at[idx, "行動班"] = new_act
                            has_act_changed = True
                if has_act_changed:
                    st.session_state["p3_data"] = df_p3
                    st.rerun()
                st.markdown("---")

            cols = st.columns(max(len(act_groups), 1))
            for idx, grp in enumerate(act_groups):
                with cols[idx]:
                    grp_df = df_p3[df_p3["行動班"] == grp]
                    st.markdown(f"### 行動班 {grp}")
                    st.write(f"**人数:** {len(grp_df)}名")
                    st.write(
                        f"**男女比:** 男{len(grp_df[grp_df['性別']=='男'])}名 / 女{len(grp_df[grp_df['性別']=='女'])}名"
                    )
                    st.write(
                        f"**学年比:** 1年{len(grp_df[grp_df['学年']==1])}名 / 2年{len(grp_df[grp_df['学年']==2])}名 / 3年{len(grp_df[grp_df['学年']==3])}名"
                    )

                    disp_grp = grp_df[["名前", "学年", "性別", "係"]].copy()
                    disp_grp["係"] = disp_grp["係"].apply(serialize_list_col)
                    st.dataframe(disp_grp, use_container_width=True, hide_index=True)

            if edit_mode_p3:
                st.markdown("---")
                if st.button("行動班のみ保存", key="save_act"):
                    save_p3_to_gsheet(df_p3, target="act")

    with tab3:
        st.subheader("食事班詳細")
        meal_groups = sorted([g for g in df_p3["食事班"].unique() if str(g).strip() != ""])

        if not meal_groups:
            st.info("まだ食事班が割り当てられていません。「① 自動班決め実行」ボタンを押してください。")
        else:
            if edit_mode_p3:
                st.info("各生徒の食事班を変更できます。")
                has_meal_changed = False
                for idx, row in df_p3.iterrows():
                    col_name, col_sel = st.columns([1, 2])
                    with col_name:
                        st.write(
                            f"**{row['名前']}** ({row.get('性別','')}/{row.get('学年','')}年)"
                        )
                    with col_sel:
                        curr_meal = str(row.get("食事班", ""))
                        new_meal = st.selectbox(
                            f"{row['名前']} の食事班",
                            options=meal_options,
                            index=meal_options.index(curr_meal)
                            if curr_meal in meal_options
                            else 0,
                            key=f"meal_sel_{idx}_{curr_meal}",
                            label_visibility="collapsed",
                        )
                        if new_meal != curr_meal:
                            df_p3.at[idx, "食事班"] = new_meal
                            has_meal_changed = True
                if has_meal_changed:
                    st.session_state["p3_data"] = df_p3
                    st.rerun()
                st.markdown("---")

            cols = st.columns(max(len(meal_groups), 1))
            for idx, grp in enumerate(meal_groups):
                with cols[idx]:
                    grp_df = df_p3[df_p3["食事班"] == grp]
                    st.markdown(f"### 食事班 {grp}")
                    st.write(f"**人数:** {len(grp_df)}名")
                    st.write(
                        f"**男女比:** 男{len(grp_df[grp_df['性別']=='男'])}名 / 女{len(grp_df[grp_df['性別']=='女'])}名"
                    )
                    st.write(
                        f"**学年比:** 1年{len(grp_df[grp_df['学年']==1])}名 / 2年{len(grp_df[grp_df['学年']==2])}名 / 3年{len(grp_df[grp_df['学年']==3])}名"
                    )

                    disp_grp = grp_df[["名前", "学年", "性別", "係"]].copy()
                    disp_grp["係"] = disp_grp["係"].apply(serialize_list_col)
                    st.dataframe(disp_grp, use_container_width=True, hide_index=True)

            if edit_mode_p3:
                st.markdown("---")
                if st.button("食事班のみ保存", key="save_meal"):
                    save_p3_to_gsheet(df_p3, target="meal")

    with tab4:
        st.subheader("テント班詳細")
        tent_groups = sorted([
            g for g in df_p3["テント班"].dropna().unique() if str(g).strip() != ""
        ])

        if not tent_groups:
            st.info("まだテント班が割り当てられていません。「① 自動班決め実行」ボタンを押してください。")
        else:
            if edit_mode_p3:
                st.info("各生徒・大人のテント班を変更できます。未割り当ての利用可能テントも選択可能です。")
                has_tent_changed = False
                for idx, row in df_p3.iterrows():
                    col_name, col_sel = st.columns([1, 2])
                    with col_name:
                        st.write(
                            f"**{row['名前']}** ({row.get('性別','')}/{row.get('学年','')}年)"
                        )
                    with col_sel:
                        curr_tent = str(row.get("テント班", ""))
                        opts = (
                            tent_options
                            if curr_tent in tent_options
                            else tent_options + [curr_tent]
                        )
                        idx_val = opts.index(curr_tent) if curr_tent in opts else 0

                        new_tent = st.selectbox(
                            f"{row['名前']} のテント班",
                            options=opts,
                            index=idx_val,
                            key=f"tent_sel_{idx}_{curr_tent}",
                            label_visibility="collapsed",
                        )
                        if new_tent != curr_tent:
                            df_p3.at[idx, "テント班"] = new_tent
                            has_tent_changed = True
                if has_tent_changed:
                    st.session_state["p3_data"] = df_p3
                    st.rerun()
                st.markdown("---")

            if tent_groups:
                cols = st.columns(min(max(len(tent_groups), 1), 4))
                for idx, grp in enumerate(tent_groups):
                    with cols[idx % 4]:
                        grp_df = df_p3[df_p3["テント班"] == grp]
                        st.markdown(f"### テント: {grp}")
                        st.write(f"**人数:** {len(grp_df)}名")
                        st.write(
                            f"**男女比:** 男{len(grp_df[grp_df['性別']=='男'])}名 / 女{len(grp_df[grp_df['性別']=='女'])}名"
                        )
                        st.write(
                            f"**学年比:** 1年{len(grp_df[grp_df['学年']==1])}名 / 2年{len(grp_df[grp_df['学年']==2])}名 / 3年{len(grp_df[grp_df['学年']==3])}名"
                        )
                        st.dataframe(
                            grp_df[["名前", "性別", "学年"]],
                            use_container_width=True,
                            hide_index=True,
                        )

            if edit_mode_p3:
                st.markdown("---")
                if st.button("テント班のみ保存", key="save_tent"):
                    save_p3_to_gsheet(df_p3, target="tent")

    with tab5:
        st.subheader("共同装備詳細")

        has_any_gear = any(
            len(deserialize_list_col(g)) > 0 for g in df_p3["共同装備"]
        )

        if not has_any_gear:
            st.info("まだ共同装備が割り当てられていません。「② 自動共同装備振り分け実行」ボタンを押してください。")
        else:
            if edit_mode_p3:
                st.info("各メンバーの共同装備を変更できます。未割り当ての該当装備も選択肢に表示されます。")

            display_df = df_p3.copy()
            has_gear_changed = False

            other_selected_all = []
            for _, o_row in display_df.iterrows():
                other_selected_all.extend(
                    deserialize_list_col(o_row.get("共同装備", []))
                )
            global_counts = Counter(other_selected_all)

            for idx, row in display_df.iterrows():
                st_name = row["名前"]
                st_gender = str(row.get("性別", ""))
                st_grade = str(row.get("学年", ""))
                st_act = str(row.get("行動班", ""))
                st_meal = str(row.get("食事班", ""))
                st_tent = str(row.get("テント班", ""))
                st_roles = deserialize_list_col(row.get("係", []))
                curr_gear = deserialize_list_col(row.get("共同装備", []))

                curr_weight = sum([
                    i["weight"]
                    for gname in curr_gear
                    for i in item_pool
                    if i["full_name"] == gname
                ])

                info_label = f"**{st_name}** ({st_gender}/{st_grade}年/{st_act}/{st_meal}/{st_tent})"

                col_info, col_select = st.columns([1, 2])

                with col_info:
                    st.markdown(info_label)
                    st.markdown(f"**現在の合計重量: {curr_weight}**")

                with col_select:
                    if edit_mode_p3:
                        my_valid_options = []
                        for item in item_pool:
                            fname, ttype, tval = (
                                item["full_name"],
                                item["target_type"],
                                item["target_val"],
                            )

                            is_relevant = False
                            if ttype == "フリー":
                                is_relevant = True
                            elif ttype == "テント班" and tval == st_tent and st_tent != "":
                                is_relevant = True
                            elif ttype == "食事班" and tval == st_meal and st_meal != "":
                                is_relevant = True
                            elif ttype == "行動班" and tval == st_act and st_act != "":
                                is_relevant = True
                            elif ttype == "係" and tval in st_roles:
                                is_relevant = True

                            if not is_relevant:
                                continue

                            max_cnt = sum(
                                1 for x in item_pool if x["full_name"] == fname
                            )
                            used_cnt = global_counts.get(fname, 0)
                            if fname in curr_gear:
                                used_cnt -= 1

                            if used_cnt < max_cnt:
                                my_valid_options.append(fname)

                        my_options = sorted(list(set(my_valid_options + curr_gear)))

                        new_selected = st.multiselect(
                            f"{st_name} さんの共同装備",
                            options=my_options,
                            default=curr_gear,
                            key=f"select_gear_{idx}_{','.join(curr_gear)}",
                            label_visibility="collapsed",
                        )

                        if set(new_selected) != set(curr_gear):
                            has_gear_changed = True
                            new_weight = sum([
                                i["weight"]
                                for gname in new_selected
                                for i in item_pool
                                if i["full_name"] == gname
                            ])
                            display_df.at[idx, "共同装備"] = new_selected
                            display_df.at[idx, "重量"] = new_weight
                    else:
                        gear_str = ", ".join(curr_gear) if curr_gear else "なし"
                        st.markdown(
                            f'<div class="belongings-box">{gear_str}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown("<hr style='margin: 12px 0; border-color: #E2E8E0;'>", unsafe_allow_html=True)

            if has_gear_changed:
                st.session_state["p3_data"] = display_df
                st.rerun()

            st.markdown("---")
            st.markdown("### 個人重量グラフ")

            df_chart_prep = df_p3.copy()
            if "HRNO" in df_chart_prep.columns:
                df_chart_prep["HRNO_str"] = (
                    df_chart_prep["HRNO"].astype(str).str.zfill(4)
                )
                df_chart_prep["_hrno_num"] = pd.to_numeric(
                    df_chart_prep["HRNO"], errors="coerce"
                ).fillna(9999)
                df_chart_prep = df_chart_prep.sort_values(
                    by="_hrno_num", ascending=True
                )

            chart = (
                alt.Chart(df_chart_prep)
                .mark_bar(color="#485736")
                .encode(
                    x=alt.X("名前:N", sort=alt.EncodingSortField(field="_hrno_num", order="ascending"), title="名前（HRNO昇順）"),
                    y=alt.Y("重量:Q", title="重量"),
                    tooltip=["HRNO_str", "名前", "重量"],
                )
                .properties(height=350)
            )
            st.altair_chart(chart, use_container_width=True)

            if edit_mode_p3:
                st.markdown("---")
                if st.button("共同装備のみ保存", key="save_gear"):
                    save_p3_to_gsheet(df_p3, target="gear")

elif page == "計画書出力":
    st.markdown(
        "<h1>計画書出力</h1>", unsafe_allow_html=True
    )
    st.write("準備中")