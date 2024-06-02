page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
    background-image: url("https://media.istockphoto.com/id/669480814/photo/3d-rendering-modern-wood-gym-and-training-room-with-city-view.jpg?s=2048x2048&w=is&k=20&c=7BcCx2SjFVaXhxJM_nP_jvjQOr5NwFTVfWg8esWPMPc=");
    background-size: cover;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}
</style>
"""


info_string = """
    <div style="backdrop-filter: blur(4px)">
    <div style='margin-bottom: 20px;'>
        <h2 style='color: #7F00FF'>Introduction:</h2>
        <p style='font-size: 16px; color: white'>Our AI Coach program is designed to revolutionize your workout experience by providing real-time feedback on your exercise technique and automatically counting your reps. We understand the importance of maintaining proper form during workouts to prevent injuries and maximize results. With AI Coach, you can focus on perfecting your technique while our model takes care of counting your reps and providing feedback.</p>
    </div>

    <div style='margin-bottom: 20px;'>
        <h2 style='color: #7F00FF'>Features:</h2>
        <p style='font-size: 16px; color: white;'>- Rep Counting: Our AI model accurately counts your reps during workouts, allowing you to focus on your form and technique.</p>
        <p style='font-size: 16px; color: white;'>- Technique Feedback: Receive instant feedback on your exercise technique to ensure you're performing each movement correctly and safely.</p>
        <p style='font-size: 16px; color: white;'>- Progress Tracking: Monitor your progress over time and see how your performance improves with each workout session.</p>
        <p style='font-size: 16px; color: white;'>- Calorie Calculator: Use our calorie calculator to determine your daily calorie needs to maintain your weight.</p>
    </div>

    <div style='margin-bottom: 20px'>
        <h2 style='color: #7F00FF;'>How it Works:</h2>
        <p style='font-size: 16px; color: white;'>AI Coach utilizes state-of-the-art machine learning algorithms to analyze your movements during workouts. By comparing your actions to established exercise techniques, our model provides real-time feedback to help you maintain proper form and maximize your workout efficiency.</p>
    </div>

    <div style='margin-bottom: 20px'>
        <h2 style='color: #7F00FF;'>Purpose:</h2>
        <p style='font-size: 16px; color: white;'>Our app is designed to help users improve their athletic performance and achieve their fitness goals. We believe that by providing personalized coaching and support, we can empower individuals to reach their full potential and lead healthier, happier lives.</p>
    </div>

    <div style='margin-bottom: 20px'>
        <h2 style='color: #7F00FF;'>Contact Information:</h2>
        <p style='font-size: 16px; color: white;'>For inquiries or support, please email us at <a href="mailto:nurzhanov0504@gmail.com" style='color: cobalt;'>nurzhanov0504@gmail.com</a>.</p>
    </div>
    
    </div>
"""




login_page_else_string = f"""
        <style>
            .blur-text {{
                text-align: center;
                font-size: 1.5em;
                color: #333; /* Darker text for better contrast */
                background: rgba(255, 255, 255, 0.8); /* Slightly more opaque background */
                backdrop-filter: blur(4px);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for better separation */
                margin-top: 20px; /* Space from the top */
            }}
        </style>
        <div class='blur-text'>
            <p><strong>You are already logged in to your account.</strong></p>
            <p>You are free to explore and use all the features of the site, including tracking your progress, accessing the AI coach, and viewing the top users.</p>
        </div>
    """

account_info_page_else_string = f"""
        <style>
            .blur-text {{
                text-align: center;
                font-size: 1.5em;
                color: #333; /* Darker text for better contrast */
                background: rgba(255, 255, 255, 0.8); /* Slightly more opaque background */
                backdrop-filter: blur(4px);
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for better separation */
                margin-top: 20px; /* Space from the top */
            }}
        </style>
        <div class='blur-text'>
            <p><strong>To use the "Account Info" page, you need to register or log in first.</strong></p>
            <p>Once logged in, you'll be able to see your account info, track your progress, and view other top users on the site.</p>
        </div>
    """

ai_coach_else_string = f"""
    <style>
        .blur-text {{
            text-align: center;
            font-size: 1.5em;
            color: #333; /* Darker text for better contrast */
            background: rgba(255, 255, 255, 0.8); /* Slightly more opaque background */
            backdrop-filter: blur(4px);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for better separation */
            margin-top: 20px; /* Space from the top */
        }}
    </style>
    <div class='blur-text'>
        <p><strong>To use the AI Coach, you need to register or log in first.</strong></p>
        <p>Once logged in, you'll be able to access a coach to start your workout. The coach will count your reps and sets, and provide feedback on your mistakes.</p>
    </div>
"""