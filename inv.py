import time
import streamlit as st
from google import genai

# ============================================================
# GEMINI API KEY
# ============================================================

API_KEY = "AQ.Ab8RN6IQsja9iZJV19aNNq9SwbLW8iesxP2R-u1A5jh1wOwhTw"

client = genai.Client(api_key=API_KEY)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Inventor",
    page_icon="💡",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("💡 AI Inventor")

st.subheader(
    "Turn everyday objects into innovative inventions"
)

st.write(
    "📷 Take a photo using your camera OR 📁 upload an image "
    "and let AI transform it into a new invention."
)

st.divider()

# ============================================================
# CAMERA
# ============================================================

st.header("📷 Take a Photo")

camera_photo = st.camera_input(
    "Open Camera"
)

# ============================================================
# IMAGE UPLOAD
# ============================================================

st.header("📁 Or Upload an Image")

uploaded_photo = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"]
)

# ============================================================
# SELECT IMAGE
# ============================================================

image_file = None

if camera_photo is not None:
    image_file = camera_photo

elif uploaded_photo is not None:
    image_file = uploaded_photo

# ============================================================
# DISPLAY IMAGE
# ============================================================

if image_file is not None:

    st.divider()

    st.image(
        image_file,
        caption="Selected Object",
        width=450
    )

    st.divider()

    # ========================================================
    # INVENT BUTTON
    # ========================================================

    if st.button(
        "🚀 INVENT SOMETHING",
        use_container_width=True
    ):

        with st.spinner(
            "🧠 AI is analyzing your object..."
        ):

            try:

                image_bytes = image_file.getvalue()

                # ====================================================
                # AI PROMPT
                # ====================================================

                prompt = """
You are an advanced AI inventor, product designer,
engineer and creative problem solver.

Analyze the uploaded image carefully.

Identify the main object in the image.

Then create ONE highly creative, useful and realistic
invention inspired by that object.

IMPORTANT:
- Do NOT give a boring modification.
- Do NOT simply add a common feature.
- Think of an unexpected but useful application.
- Focus on solving a real-world problem.
- The invention should be technically realistic.
- Make the concept exciting and innovative.

Return the answer using exactly this structure:

🔎 OBJECT IDENTIFIED
Name of the object.

💡 INVENTION NAME
Give the invention a unique and memorable name.

🚀 THE BIG IDEA
Explain the invention clearly in 3-5 sentences.

🎯 PROBLEM IT SOLVES
Explain the real-world problem it solves.

⚙️ HOW IT WORKS
Explain the invention step-by-step.

🧰 MATERIALS REQUIRED
List the required materials and components.

💰 ESTIMATED COST
Give an approximate cost in Indian Rupees.

📊 DIFFICULTY
Easy / Medium / Hard

🌍 REAL-WORLD USE
Explain who can use this invention and where it can be useful.

🛡️ SAFETY
Mention important safety precautions.

🔄 ALTERNATIVE VERSION
Give another possible version of the invention.

🤖 AI / TECHNOLOGY UPGRADE
Explain how AI, sensors, IoT, computer vision,
robotics, automation or smart technology could improve it.

🔥 WHY THIS IS INNOVATIVE
Explain what makes this invention different from
ordinary products.

🚀 FUTURE POSSIBILITY
Explain how this idea could become a real product
in the future.

Be highly creative, practical and technically realistic.
"""

                # ====================================================
                # GEMINI REQUEST WITH RETRY
                # ====================================================

                response = None

                for attempt in range(3):

                    try:

                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=[
                                prompt,
                                {
                                    "inline_data": {
                                        "mime_type": image_file.type,
                                        "data": image_bytes
                                    }
                                }
                            ]
                        )

                        break

                    except Exception as e:

                        error_message = str(e)

                        if (
                            "503" in error_message
                            or "UNAVAILABLE" in error_message
                        ):

                            if attempt < 2:

                                time.sleep(5)

                            else:

                                st.error(
                                    "⚠️ Gemini is currently experiencing "
                                    "high demand. Please wait a little "
                                    "and try again."
                                )

                                st.stop()

                        else:

                            raise e

                # ====================================================
                # DISPLAY RESULT
                # ====================================================

                if response is not None:

                    st.success(
                        "🎉 Your invention is ready!"
                    )

                    st.divider()

                    st.markdown(
                        response.text
                    )

            except Exception as e:

                st.error(
                    "❌ Something went wrong."
                )

                st.code(
                    str(e)
                )