import streamlit as st
import random

st.set_page_config(page_title="Hand Cricket Game", page_icon="🏏")
st.title("🏏 Hand Cricket Game")

# --- Initialize session state variables ---
if "toss_done" not in st.session_state:
    st.session_state.toss_done = False
if "user_choice" not in st.session_state:
    st.session_state.user_choice = None
if "target" not in st.session_state:
    st.session_state.target = None
if "innings" not in st.session_state:
    st.session_state.innings = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- Step 1: Toss ---
st.subheader("Toss Time 🎲")
choice = st.radio("Choose HEADS or TAILS:", ["Heads", "Tails"])
play_btn = st.button("Play Toss")

if play_btn and not st.session_state.toss_done:
    toss_result = random.choice(["Heads", "Tails"])
    st.write(f"Toss Result: **{toss_result}**")

    if choice == toss_result:
        st.success("You won the toss!")
        st.session_state.user_choice = st.radio(
            "Do you want to Bat or Bowl?", ["Bat", "Bowl"], key="bat_bowl_choice"
        )
        if st.button("Confirm Choice"):
            st.session_state.toss_done = True
    else:
        st.error("You lost the toss!")
        st.session_state.user_choice = random.choice(["Bat", "Bowl"])
        st.write(f"CPU chooses to **{st.session_state.user_choice}** first.")
        st.session_state.toss_done = True


# --- Step 2 & 3: Innings ---
if st.session_state.toss_done and not st.session_state.game_over:
    st.subheader(f"Innings {st.session_state.innings}")

    user_num = st.number_input("Enter a number (1-6):", min_value=1, max_value=6, step=1)
    play_ball = st.button("Play Ball")

    if play_ball:
        cpu_num = random.randint(1, 6)
        st.write(f"You: {user_num} | CPU: {cpu_num}")

        if user_num == cpu_num:  # Wicket
            st.warning("Wicket!")

            if st.session_state.innings == 1:  # End of first innings
                st.session_state.target = st.session_state.score + 1
                st.write(f"🎯 Target is {st.session_state.target}")
                st.session_state.innings = 2
                st.session_state.score = 0
            else:  # End of second innings
                st.session_state.game_over = True
        else:
            if (st.session_state.user_choice == "Bat" and st.session_state.innings == 1) or \
               (st.session_state.user_choice == "Bowl" and st.session_state.innings == 2):
                st.session_state.score += user_num
            else:
                st.session_state.score += cpu_num

        st.write(f"Current Score: {st.session_state.score}")

        # Check win condition in 2nd innings
        if st.session_state.innings == 2 and st.session_state.score >= st.session_state.target:
            st.success("🎉 Target chased! Winner!")
            st.session_state.game_over = True

# --- End of Game ---
if st.session_state.game_over:
    st.subheader("🏁 Game Over")
    st.write(f"Final Score: {st.session_state.score}")
    if st.session_state.innings == 2 and st.session_state.score >= st.session_state.target:
        st.success("🎉 Target chased! Winner!")
    else:
        st.error("❌ All out! Loser!")

    if st.button("🔄 Restart Game"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
