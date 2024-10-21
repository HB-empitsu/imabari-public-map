import pandas as pd
from streamlit_folium import st_folium

import folium
import folium.plugins
import streamlit as st


@st.cache_data
def load_data():
    df = pd.read_csv("今治市施設一覧.csv")
    return df


st.set_page_config(page_title="今治市施設一覧", layout="wide")
st.title("今治市施設一覧")

df0 = load_data()

themes = df0["テーマ"].unique().tolist()


option = st.selectbox("テーマを選択してください", themes)

if option:
    df1 = df0[df0["テーマ"] == option].copy()

    lat = df1["緯度"].mean()
    lng = df1["経度"].mean()

    # フォリウムマップの初期化
    m = folium.Map(
        location=[lat, lng],
        tiles="https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://maps.gsi.go.jp/development/ichiran.html">国土地理院</a>',
        zoom_start=10,
    )

    # データフレームからマーカーを追加
    for _, row in df1.iterrows():
        folium.Marker(
            location=[row["緯度"], row["経度"]],
            popup=folium.Popup(
                f'<p>{row["分類"]}</p><p><a href="{row["リンク"]}" target="_blank">{row["名称"]}</a></p><p>{row["所在地"]}</p>',
                max_width=300,
            ),
            tooltip=row["名称"],
        ).add_to(m)

    # 現在値
    folium.plugins.LocateControl().add_to(m)

    # マップをストリームリットに表示
    st_data = st_folium(m, use_container_width=True, height=500)

    # 結果を表示
    df2 = df1[["名称", "所在地", "分類", "リンク"]].reset_index(drop=True)
    st.dataframe(
        df2,
        use_container_width=True,
        hide_index=True,
        column_config={
            "リンク": st.column_config.LinkColumn(),
        },
    )
