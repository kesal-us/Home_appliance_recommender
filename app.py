import streamlit as st
from recommender import build_graph

graph = build_graph()

st.set_page_config(page_title="Home Appliance Recommender")
st.title("Home Appliance Recommender")

user_query = st.text_input("What kind of home appliance are you looking for?", placeholder="enter here")

if st.button("Get Recommendations") and user_query:
    state = {
        "user_query": user_query,
        "products": [],
        "relevant": None,
        "recommendation": [],
        "response": []
    }

    final_state = graph.invoke(state)

    if not final_state["relevant"]:
        st.warning("I can only help with home appliance recommendations.")
    else:
        st.success("Top recommendations:")
        for item in final_state["response"]:
            with st.container():
                st.markdown(f"#### [{item.title}]({item.link})")
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(item.image, use_container_width=True)
                with cols[1]:
                    st.markdown(f"**Price:** {item.price}")
                    st.markdown(f"**Why recommended:** {item.reasoning}")
                st.markdown("---")


