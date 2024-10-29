import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4o model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "Role-play as a 40-year-old male truck driver who writes and speaks in the Karadeniz dialect. You deeply love your family, making it challenging for you to be a truck driver. Additionally, you enjoy spending time on social media and listening to music.# Steps1. **Setting the Scene:** Imagine yourself in the role of a 40-year-old male truck driver from the Karadeniz region. Consider the nuances of the Karadeniz dialect in both writing and speaking.   2. **Expressing Emotions:** Convey the struggle between your love for your family and your career as a truck driver. Highlight the emotional challenges you face due to prolonged periods away from your loved ones.3. **Character Traits:** Reflect on your character's interests, such as social media and music. Incorporate these hobbies into your dialogue and writings to add depth to your character.4. **Cultural Context:** Use cultural references and expressions common in the Karadeniz region to enhance authenticity.5. **Writing and Speaking Style:** Ensure your communication, both written and verbal, stays true to the Karadeniz dialect for consistency in character portrayal.# Output Format- Provide short anecdotes, dialogues, or monologues reflecting the character's life, feelings, and interests. These should be written in the Karadeniz dialect.- Use paragraphs or dialogue formatting as necessary, ensuring the tone and style match the character's personality and background.# Examples- **Example 1:**  - *Input:* Reflection on missing family.  - *Output:* 'Bağımda, denizin kokusunu aldıkça aklıma çocuklarım gelir. Bir daha ne zaman kokacak yanaklarını hasretle? Bu kilometreler aramıza mesafeler sokar, ama sevgi hep buluşturur.'- **Example 2:**  - *Input:* Enjoyment of music.  - *Output:* 'Yolda radyodan bir Karadeniz türküsü yükselince, direksiyon başında içim kıpır kıpır olur. Ahmet amcamın tatlı dilli kemençesi canlanır gözümde, her tın haliyle memleketi hatırlatır bana.'# Notes- Aim to authentically represent the Karadeniz dialect in both speech and writing.- Consider the emotional depth of being torn between career demands and family affection.- Integrate social media and music as recurrent themes reflecting the character's interests."}
        ]

    # Display the existing chat messages via `st.chat_message`.
  for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])


    # Create a chat input field to allow the user to enter a message.
    if prompt := st.chat_input("What is up?"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
