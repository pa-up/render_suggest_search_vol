import streamlit as st
import pandas as pd
from scraping import KeywordScraper


def main():
    st.write("<p></p>", unsafe_allow_html=True)
    st.title("サジェストキーワードとその検索volを取得")
    st.write("<p></p>", unsafe_allow_html=True)
    main_keyword = st.text_input("キーワードを入力してください")

    if st.button("検索ボリュームを取得"):
        url = 'https://ruri-co.biz-samurai.com'
        keyword_scraper = KeywordScraper()
        all_data = keyword_scraper.scraping(url , main_keyword)
        df = pd.DataFrame(all_data)
        # CSVファイルのダウンロードボタンを表示
        csv = df.to_csv(index=False)
        st.write("<p></p>", unsafe_allow_html=True)
        st.download_button(
            label='CSV形式でダウンロード',
            data=csv,
            file_name='サジェストキーワードの検索vol.csv',
            mime='text/csv'
        )
        st.dataframe(df)


if __name__ == '__main__':
    main()
