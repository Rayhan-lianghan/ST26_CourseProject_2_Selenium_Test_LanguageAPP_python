import os
import webbrowser
from threading import Timer
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import models

app = Flask(__name__)
app.secret_key = 'czu_semester_6_final_testing_suite'

# Initialize database schema
models.init_db()

# Exactly 20 unique core words per lesson (60 total)
LESSONS_DATA = {
    "1": [
        {"id": 1, "word": "我", "pinyin": "wǒ", "english": "I / Me", "sentence": "我在常州大学学习。", "translation": "I study at Changzhou University."},
        {"id": 2, "word": "你", "pinyin": "nǐ", "english": "You", "sentence": "很高兴在这里认识你。", "translation": "Nice to meet you here."},
        {"id": 3, "word": "是", "pinyin": "shì", "english": "To be / Yes", "sentence": "汉语水平考试是非常重要的考试。", "translation": "The HSK is a very important exam."},
        {"id": 4, "word": "在", "pinyin": "zài", "english": "In / At / On", "sentence": "老师正在办公室等我们。", "translation": "The teacher is waiting for us in the office."},
        {"id": 5, "word": "好", "pinyin": "hǎo", "english": "Good / Well", "sentence": "只要多练习，你的汉语就会变好。", "translation": "As long as you practice more, your Chinese will get better."},
        {"id": 6, "word": "看", "pinyin": "kàn", "english": "To look / Read", "sentence": "请看看这个句子怎么读。", "translation": "Please look at how to read this sentence."},
        {"id": 7, "word": "学生", "pinyin": "xue sheng", "english": "Student", "sentence": "留学生们都在准备考试。", "translation": "The international students are all preparing for the exam."},
        {"id": 8, "word": "老师", "pinyin": "lǎo shī", "english": "Teacher", "sentence": "我们的汉语老师非常认真。", "translation": "Our Chinese teacher is very conscientious."},
        {"id": 9, "word": "学校", "pinyin": "xué xiào", "english": "School", "sentence": "常州大学是一个美丽的学校。", "translation": "Changzhou University is a beautiful school."},
        {"id": 10, "word": "朋友", "pinyin": "péng you", "english": "Friend", "sentence": "我在班里交到了很多好朋友。", "translation": "I made many good friends in my class."},
        {"id": 11, "word": "听", "pinyin": "tīng", "english": "To listen", "sentence": "听力考试的时候需要非常集中。", "translation": "You need to be very focused during the listening test."},
        {"id": 12, "word": "说", "pinyin": "shuō", "english": "To speak", "sentence": "请用汉语说一说你的想法。", "translation": "Please say your ideas in Chinese."},
        {"id": 13, "word": "读", "pinyin": "dú", "english": "To read / Read aloud", "sentence": "这篇课文请大家大声读出来。", "translation": "Everyone please read this text out loud."},
        {"id": 14, "word": "写", "pinyin": "xiě", "english": "To write", "sentence": "我每天都要练习写汉字。", "translation": "I practice writing Chinese characters every day."},
        {"id": 15, "word": "汉字", "pinyin": "hàn zì", "english": "Chinese character", "sentence": "这个汉字的意思很容易懂。", "translation": "The meaning of this Chinese character is easy to understand."},
        {"id": 16, "word": "有", "pinyin": "yǒu", "english": "To have", "sentence": "我们明天有一堂重要的测试课。", "translation": "We have an important testing class tomorrow."},
        {"id": 17, "word": "喜欢", "pinyin": "xǐ huan", "english": "To like", "sentence": "我很喜欢在常州生活和学习。", "translation": "I really like living and studying in Changzhou."},
        {"id": 18, "word": "谢谢", "pinyin": "xiè xie", "english": "To thank / Thanks", "sentence": "谢谢同学帮我指出了代码的错误。", "translation": "Thank you classmate for pointing out my code error."},
        {"id": 19, "word": "再见", "pinyin": "zài jiàn", "english": "Goodbye", "sentence": "考完试后我们和老师说再见。", "translation": "We say goodbye to the teacher after finishing the exam."},
        {"id": 20, "word": "明天", "pinyin": "míng tiān", "english": "Tomorrow", "sentence": "明天早上我们要提交最终报告。", "translation": "Tomorrow morning we need to submit the final report."}
    ],
    "2": [
        {"id": 21, "word": "考试", "pinyin": "kǎo shì", "english": "Exam / Test", "sentence": "顺利通过这次考试就能安心毕业。", "translation": "Passing this exam smoothly means you can graduate peacefully."},
        {"id": 22, "word": "学习", "pinyin": "xué xí", "english": "To study / Learn", "sentence": "学习编程需要不断地敲代码。", "translation": "Learning programming requires continuously typing code."},
        {"id": 23, "word": "帮助", "pinyin": "bāng zhù", "english": "To help / Assist", "sentence": "同学之间的互相帮助非常重要。", "translation": "Mutual help among classmates is very important."},
        {"id": 24, "word": "容易", "pinyin": "róng yì", "english": "Easy", "sentence": "这个黑盒测试用例编写起来很容易。", "translation": "This black-box test case is very easy to write."},
        {"id": 25, "word": "懂", "pinyin": "dǒng", "english": "To understand", "sentence": "老师讲的系统架构我都听懂了。", "translation": "I understood the system architecture explained by the teacher."},
        {"id": 26, "word": "准备", "pinyin": "zhǔn bèi", "english": "To prepare", "sentence": "我们在为下周的期末项目做准备。", "translation": "We are preparing for next week's final project."},
        {"id": 27, "word": "高兴", "pinyin": "gāo xìng", "english": "Happy / Glad", "sentence": "听到考试通过的消息，大家都很高兴。", "translation": "Everyone was very happy to hear the news of passing the exam."},
        {"id": 28, "word": "觉得", "pinyin": "jué de", "english": "To think / Feel", "sentence": "我觉得这套刷题系统非常好用。", "translation": "I think this quiz system is very useful."},
        {"id": 29, "word": "知道", "pinyin": "zhī dào", "english": "To know", "sentence": "你知道怎么配置自动启动的脚本吗？", "translation": "Do you know how to configure the auto-start script?"},
        {"id": 30, "word": "希望", "pinyin": "xī wàng", "english": "To hope", "sentence": "我希望大家都能取得优异的成绩。", "translation": "I hope everyone can achieve excellent results."},
        {"id": 31, "word": "开始", "pinyin": "kāi shǐ", "english": "To start / Begin", "sentence": "测试用例自动化将在五秒后开始。", "translation": "Test case automation will start in five seconds."},
        {"id": 32, "word": "时间", "pinyin": "shí jiān", "english": "Time", "sentence": "我们的系统测试时间只有四十五分钟。", "translation": "Our system testing time is only forty-five minutes."},
        {"id": 33, "word": "题", "pinyin": "tí", "english": "Question / Problem", "sentence": "这道选择题的答案是一号选项。", "translation": "The answer to this multiple-choice question is option number one."},
        {"id": 34, "word": "意思", "pinyin": "yì si", "english": "Meaning", "sentence": "这句话的意思我还没完全搞明白。", "translation": "I haven't fully figured out the meaning of this sentence yet."},
        {"id": 35, "word": "锻炼", "pinyin": "duàn liàn", "english": "To exercise / Train", "sentence": "学习之余，也要经常去操场锻炼。", "translation": "Besides studying, you should also often exercise on the sports field."},
        {"id": 36, "word": "身体", "pinyin": "shēn tǐ", "english": "Health / Body", "sentence": "保持身体健康才能更好地写代码。", "translation": "Keeping healthy is the only way to write code better."},
        {"id": 37, "word": "经常", "pinyin": "jīng cháng", "english": "Often", "sentence": "我们经常在实验室里讨论算法题。", "translation": "We often discuss algorithm questions in the lab."},
        {"id": 38, "word": "特别", "pinyin": "tè bié", "english": "Especially", "sentence": "今天的自动化测试课特别有意思。", "translation": "Today's automated testing class was especially interesting."},
        {"id": 39, "word": "注意", "pinyin": "zhù yì", "english": "To pay attention", "sentence": "提交表单时请注意手机号的格式。", "translation": "Please pay attention to the phone number format when submitting the form."},
        {"id": 40, "word": "努力", "pinyin": "nǔ lì", "english": "Hard-working / Effort", "sentence": "只有努力付出，才会有美好的未来。", "translation": "Only by putting in effort will there be a beautiful future."}
    ],
    "3": [
        {"id": 41, "word": "毕业", "pinyin": "bì yè", "english": "To graduate", "sentence": "通过HSK四级是我们在常大毕业的前提。", "translation": "Passing HSK 4 is a prerequisite for our graduation from CZU."},
        {"id": 42, "word": "证书", "pinyin": "zhèng shū", "english": "Certificate", "sentence": "毕业时我们需要拿到学位证书。", "translation": "We need to get our degree certificate when graduating."},
        {"id": 43, "word": "要求", "pinyin": "yāo qiú", "english": "Requirement", "sentence": "系统的功能性要求已经全部实现。", "translation": "All functional requirements of the system have been implemented."},
        {"id": 44, "word": "感谢", "pinyin": "gǎn xiè", "english": "To thank / Grateful", "sentence": "非常感谢教授对我们项目的悉心指导。", "translation": "Thank you very much, Professor, for your careful guidance on our project."},
        {"id": 45, "word": "进步", "pinyin": "jìn bù", "english": "Progress", "sentence": "经过一学期的训练，他的汉语进步很大。", "translation": "After a semester of training, his Chinese has made great progress."},
        {"id": 46, "word": "留学生", "pinyin": "liú xué shēng", "english": "International student", "sentence": "常大有很多来自不同国家的留学生。", "translation": "CZU has many international students from different countries."},
        {"id": 47, "word": "水平", "pinyin": "shuǐ píng", "english": "Level / Proficiency", "sentence": "编程水平是通过实践不断提高的。", "translation": "Programming proficiency is continuously improved through practice."},
        {"id": 48, "word": "提高", "pinyin": "tí gāo", "english": "To improve / Raise", "sentence": "这套系统可以帮助你快速提高词汇量。", "translation": "This system can help you quickly improve your vocabulary size."},
        {"id": 49, "word": "机会", "pinyin": "jī huì", "english": "Opportunity", "sentence": "这是一个非常难得的实习机会。", "translation": "This is a very rare internship opportunity."},
        {"id": 50, "word": "成功", "pinyin": "chéng gōng", "english": "Success / Succeed", "sentence": "项目成功上线运行，大家辛苦了。", "translation": "The project was successfully launched; thanks for your hard work everyone."},
        {"id": 51, "word": "简历", "pinyin": "jiǎn lì", "english": "Resume / CV", "sentence": "找工作前需要精心修改个人简历。", "translation": "You need to carefully revise your personal resume before looking for a job."},
        {"id": 52, "word": "面试", "pinyin": "miàn shì", "english": "Interview", "sentence": "明天下午有一场软件工程师的面试。", "translation": "There is a software engineer interview tomorrow afternoon."},
        {"id": 53, "word": "专业", "pinyin": "zhuān yè", "english": "Major / Profession", "sentence": "我们的专业是计算机科学与技术。", "translation": "Our major is Computer Science and Technology."},
        {"id": 54, "word": "计算机", "pinyin": "jì suàn jī", "english": "Computer", "sentence": "计算机网络是这学期的必修课。", "translation": "Computer Networks is a compulsory course this semester."},
        {"id": 55, "word": "规定", "pinyin": "guī dìng", "english": "Regulation / Rule", "sentence": "请严格遵守学校的教务管理规定。", "translation": "Please strictly abide by the university's management regulations."},
        {"id": 56, "word": "必须", "pinyin": "bì xū", "english": "Must / Essential", "sentence": "密码字段在注册时是必须填写的。", "translation": "The password field must be filled in during registration."},
        {"id": 57, "word": "改变", "pinyin": "gǎi biàn", "english": "To change", "sentence": "人工智能正在彻底改变我们的生活。", "translation": "Artificial intelligence is completely changing our lives."},
        {"id": 58, "word": "顺利", "pinyin": "shùn lì", "english": "Smoothly / Successfully", "sentence": "祝愿大家都能顺利通过期末答辩。", "translation": "Wish everyone can smoothly pass the final defense."},
        {"id": 59, "word": "影响", "pinyin": "yǐng xiǎng", "english": "Influence / Effect", "sentence": "缓存机制会直接影响系统的响应时间。", "translation": "The caching mechanism directly affects the system response time."},
        {"id": 60, "word": "未来", "pinyin": "wèi lái", "english": "Future", "sentence": "我们对计算机科学的未来充满信心。", "translation": "We are fully confident in the future of computer science."}
    ]
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        gender = request.form.get('gender')
        
        if not (username and password and email and phone and gender):
            flash("All fields are required!", "danger")
            return render_template('signup.html')
            
        if models.create_user(username, password, email, phone, gender):
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash("Username already exists!", "danger")
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = models.get_user(username)
        if not user:
            flash("User does not exist! Please create an account.", "danger")
            return render_template('login.html')
            
        if user['password'] == password:
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash("Incorrect password!", "danger")
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = models.get_user(session['username'])
    return render_template('dashboard.html', user=user)

@app.route('/lesson1')
def lesson1():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = models.get_user(session['username'])
    return render_template('lesson1.html', lessons=LESSONS_DATA["1"], user=user)

@app.route('/lesson2')
def lesson2():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = models.get_user(session['username'])
    return render_template('lesson2.html', lessons=LESSONS_DATA["2"], user=user)

@app.route('/lesson3')
def lesson3():
    if 'username' not in session:
        return redirect(url_for('login'))
    user = models.get_user(session['username'])
    return render_template('lesson3.html', lessons=LESSONS_DATA["3"], user=user)

@app.route('/toggle-favorite', methods=['POST'])
def toggle_favorite():
    if 'username' not in session:
        return jsonify({"status": "unauthorized"}), 401
    word = request.json.get('word')
    user = models.get_user(session['username'])
    fav_list = [f.strip() for f in user['favorites'].split(',') if f.strip()]
    
    if word in fav_list:
        fav_list.remove(word)
    else:
        fav_list.append(word)
        
    models.update_favorites(session['username'], ",".join(fav_list))
    return jsonify({"status": "success", "favorites": fav_list})

@app.route('/practice')
def practice():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('practice.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        score = 0
        if q1 == 'A': score += 50
        if q2 == 'B': score += 50
        models.update_quiz_score(session['username'], score)
        return redirect(url_for('dashboard'))
    return render_template('quiz.html')

@app.route('/search')
def search():
    if 'username' not in session:
        return redirect(url_for('login'))
    query = request.args.get('q', '').strip()
    results = []
    if query:
        for lid in ['1', '2', '3']:
            for w in LESSONS_DATA[lid]:
                if query.lower() in w['word'].lower() or query.lower() in w['english'].lower():
                    results.append(w)
    return render_template('search.html', query=query, results=results)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def launch_chrome_instance():
    target_url = "http://127.0.0.1:5000/"
    try:
        webbrowser.get('chrome').open_new(target_url)
    except webbrowser.Error:
        webbrowser.open_new(target_url)

if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1.0, launch_chrome_instance).start()
        
    app.run(debug=True, port=5000)