# Reversi Project Template

You must read fully and carefully the assignment specification and instructions detailed in this file. You are NOT to modify this file in any way.

* **Course:** [COMP90054 AI Planning for Autonomy](https://handbook.unimelb.edu.au/subjects/comp90054) @ Semester 2, 2022
* **Instructor:** Dr. Nir Lipovetzky and Prof. Adrian Pearce
* **Deadline Team Registration:** Monday 19th September, 2022 @ 11:59pm (start of Week 9)
* **Deadline Preliminary Submission:** Monday 3rd October, 2022 @ 11:59pm (start of Week 10)
* **Deadline Wiki, Video & Final Submission:** Monday 17th October, 2022 @ 11:59pm (start of Week 12)
* **Course Weight:** 5% (preliminary competition) + 10% (final competition) + 5% (video) + 15% (Wiki)
* **Assignment type:**: Groups of 3
* **CLOs covered:** 1-5
* **Submission method:** via git tagging (see below for instructions)

The purpose of this project is to implement a Reversi Autonomous Agent that can play and compete in the UoM COMP90054-2022 Reversi:

 <p align="center"> 
    <img src="img/sample.png" alt="sample image for GUI" width="505">
 </p>
 
 **Please read carefully the rules of the [Reversi game](https://cdn.1j1ju.com/medias/7f/91/ba-reversi-rulebook.pdf)**. Reversi can be understood as a deterministic two-players game. Understanding it well and designing a controller for it is part of the expectations for this project. Additional technical information on the contest project and how to get started can be found in file [reversi.md](Reversi/reversi.md). 

### Table of contents

  * [1. Your task](#1-your-task)
     * [Important basic rules](#important-basic-rules)
  * [2. Deliverables and submission](#2-deliverables-and-submission)
     * [Preliminary submission (Monday week 10)](#preliminary-submission-monday-week-10)
     * [Wiki and Final submission (Monday week 12)](#wiki-and-final-submission-monday-week-12)
     * [Video (Thursday week 12)](#video-thursday-week-12)
     * [Q&As](#questions-and-answers)
  * [3. Pre-contest feedback tournaments](#3-pre-contest-feedback-tournaments)
  * [4. Marking criteria](#4-marking-criteria)
  * [5. Important information](#5-important-information)
     * [How to create the Wiki](#how-to-create-the-wiki)
     * [Corrections](#corrections)
     * [Late submissions &amp; extensions](#late-submissions--extensions)
     * [About this repo](#about-this-repo)
     * [Academic Dishonesty](#academic-dishonesty)
  * [6. COMP90054 Code of Honour &amp; Fair Play](#6-comp90054-code-of-honour--fair-play)
  * [7. Conclusion](#7-conclusion)
     * [Acknowledgements](#acknowledgements)



## 1. Your task

This is a **group project** of 2 or 3 members. Now that you have a repo, the next thing to do is to register your team in the [Project Contest Team Registration Form](https://forms.gle/d3jG93PkZx8Ag9kQ9) and tell the other students to join the team in GitHub Classroom. 

**Your first task** is to get familiar with the code by developing an simple agent based on any one of the techniques listed below. This is an **individual** task. By completing this task, your teams should be able to have 2 or 3 decent agents to play with each other. In addition, each team member should understand more about the game and code.

**Your second task** is to develop an autonomous Reversi agent team to play the **Reversi Contest** by suitably modifying file [`agents/t_XXX/myTeam.py`](agents/t_000/myTeam.py) (and maybe some other auxiliarly files you may implement). The code submitted should be internally commented at high standards and be error-free and _never crash_. 

In your final submission, you have to use at **least 2 AI-related techniques** (**2 techniques at least for groups of 3**) that have been discussed in the subject or explored by you independently, and you can combine them in any form. **We won't accept a final submission with less than 2 or 3 techniques**. Some candidate techniques that you may consider are:

1. Blind or Heuristic Search Algorithms (using general or Reversi specific heuristic functions).
2. Classical Planning (PDDL and calling a classical planner).
3. Policy iteration or Value Iteration (Model-Based MDP).
4. Monte Carlo Tree Search or UCT (Model-Free MDP).
5. Reinforcement Learning – classical, approximate or deep Q-learning (Model-Free MDP).
6. Goal Recognition techniques (to infer intentions of opponents).
7. Game Theoretic Methods.


We recommend you to start by using search algorithms, given that you already implemented their code in the first project. You can always use **hand coded decision trees** to express behaviour specific to Reversi, but they **won't** count as a required technique. You are allowed to express domain knowledge, but remember that we are interested in "autonomy", and hence using techniques that generalise well. The 7 techniques mentioned above can cope with different games much easier than any decision tree (if-else rules). If you decide to compute a policy, you can save it into a file and load it at the beginning of the game, as you have 15 seconds before every game to perform any pre-computation.

Together with your actual code solution, you will need to develop a **Wiki**, documenting and describing your solution (a 5-min recorded video will also be required, see below).
 
### Important basic rules 

When submitting a solution, please make absolutely sure you adhere to the following rules:

* Please commit your own code with your **own GitHub account**. This is extremely important as the teaching team might use your commit history to evaluate your code contribution in the group.

* All your code should be in your submission directory (`agents/t_XXX/`). *XXX* in **t_XXX** should be replaced with your Canvas Team id. It should be exact three digits starting with 0. For example, if your team name in the Canvas is "Canvas Team 1", then you should create a new folder in your repo with directory as "`agents/t_001/`" and put all your code there.

* Your code **must run _error-free_ on Python 3.8+**. Staff will not debug/fix any code. If your code crashes in any execution, it will be disqualified from the contest. We provide docker config for you to test your code in the same docker environment that servers run, which you can find instructions in [reversi.md](Reversi/reversi.md) In addition, we might add more packages to the [requirement.txt](requirement.txt) daily based on request. You can either find it in the [public template repo](https://github.com/COMP90054-2022S2/comp90054-a3-reversi.git) or in the ED [announcement](https://edstem.org/au/courses/9418/discussion/1017552). 

* Your code **must not contain any personal information**, like your student number or your name. If you use an IDE that inserts your name, student number, or username, you should disable that.

* You are **not to change or affect (e.g., redirect) the standard output or error channels** (`sys.stdout` and `sys.stderr`) beyond just printing on standard output. If your file mentions any of them it will be breaking the "fair play" of the course (see below). These are used to report each game output and errors, and they should not be altered as you will be interfering negatively with the contest and with the other team's printouts. 

* Being a group assignment, you must **use your project Github** repository and GitHub team to collaborate among the members. The group will have write access to the same repository, and also be members of a GitHub team, where members can, and are expected to, engage in discussions and collaboration. Refer to the marking criteria below. 


## 2. Deliverables and submission

There will be two code submissions for this project, and one video and one report. 

### Team Registration: Monday 19th September, 2022 @ 11:59pm (start of Week 9)

Please registry your team by submitting [Project Contest Team Registration Form](https://forms.gle/d3jG93PkZx8Ag9kQ9)
### Preliminary submission (individual): Monday 3rd October, 2022 @ 11:59pm (start of Week 10)

In the **preliminary submission**, you are to:
 
1. Submit your first working version of your solution, by tagging the commit with the tag name as your student id. 
2. All your files should be in your submission directory (`agents/t_XXX/`). The file `agents/t_XXX/myTeam.py` should contain your AI-based Reversi agent as the individual agent for performance evaluation. We would highly recommend using your **own branch** for this task. 
3. We will clone your tag and run your code against a random player for 100 games. Your mark will be awarded based on your winning ratio.
4. **Please use your own github account to commit your code.** Otherwise, you would not be able to get marks.
5. Please make sure the commit in your submitted (tag) is your own original work. 


### Wiki, Video and Final submission (group): Monday 17th October, 2022 @ 11:59pm (start of Week 12)

In the **final submission** (23:59 Monday 18th October, Week 12) you are to submit your final submission to the project, which includes:


1. All your files should be in your submission directory (`agents/t_XXX/`). The file `agents/t_XXX/myTeam.py` should contain your AI-based Reversi agent as the final team agent for performance evaluation. 
2. A **Wiki** in your GitHub team repository, documenting and critically analysing your Reversi agent system. 
    * Take a look at the **Wiki** provided as a guideline of the structure that you should follow.
    * At the very minimum the Wiki should describe the approaches implemented, a small table comparing the different agents/techniques you tried showing their performances in several scenarios (briefly the table), and an analysis of the strengths and weaknesses of your solution. For example, you may want to show how the addition of a given technique or improvement affected your system at some important point in the development. 
    * However, you can also discuss other aspects, such as other techniques you experimented with (and why they were not used in the final system), future extensions or improvements on your system, etc.
3. A **Video (recorded 5-minute oral presentation)** that:
    * outlines the theoretical or experimental basis for the design of your agents (i.e. why you did what you did), challenges faced, and what you would do differently if you had more time. 
    * Your presentation must end with a live demo of your main different implementations, i.e. showing how the different techniques your tried work with some description and analysis.
    * The video will be shared with us through an unlisted youtube link at the top of the **Wiki** of your GitHub repository.
    * Please make sure your video is no longer than 5 minutes.
4. Please tag your commit with the exact tag name "`submission`". 
5. A filled [Project Certification & Contribution Form (FINAL)](https://forms.gle/gbqAaj4a2tptC79t6).
> :warning: Each member of the team should fill a separate certification form. Members who do not certify will not be marked and will be awarded zero marks.

Submit your project substantially before the deadline, preferably one day before. Submitting close to the deadline could be risky and you may fail to submit on time, for example due to loss of Internet connection or server delays. There will be **no extensions** based on these unforeseen problems. 

### Questions and Answers
* How to import other customized python files?
    * You can import with `agents.t_XXX.your_python_file_name`
* Where to save or load your local files?
    * You can open your local files with a complete relative path: `agents/t_XXX/your_file_name`. Please **do not** use `sys.path.append('agents/t_XXX/')`, which could potentially leak your path to your opponents. 



## 3. Pre-contest feedback tournaments

We will be running **informal tournaments** based on preliminary versions of teams' agents weeks before the final project submission.

Participating in these pre-contests will give you **a lot of insights** on how your solution is performing and how to improve it. Results, including replays for every game, will be available only for those teams that have submitted. 

You can re-submit multiple times, and we will just run the version tagged `test-submission`. These tournaments carry no marking at all; they are just designed for continuous feedback for you to  debug and improve your solution! You do not need to certify these versions.

We will try to run these pre-competitions frequently. The addition information about this can be found on ED later.


## 4. Marking criteria

The overall project marks (worth 50% total of the course) are as follows:

| Component | Course Weight |
| ----------| --------------|
| Performance of the preliminary submission    | 5% |
| Performance of the final submission           | 10% |
| Quality of Wiki and types of techniques used  | 15% |
| Quality of Video and types of techniques used| 5% |
| **Total** | **35%** |

### 4.1 Contests
In the final submissions, a contest will be ran using more than one game to judge the performance of each team. In the final submission (if times allows), the top-8 will enter into a playoff series to play quarterfinals, semi-finals and finals, time permitting live in the last day of class or in week 13 (once classes have finished) in a day specified for that (these final phases will not be part of the marking criteria, just bonus marks). The **performance** of your agent will be evaluated based on your ELO score.

<!-- The **performance** of your agent will be evaluated relative to some distinguished agent opponents in the contest. Distinguished agents, provided by teaching staff, will set reference levels of performance. Points will be given according to final position in the tournament with respect to such reference teams:

| Finishing above | Preliminary Contest | Final Contest |
| ----------| -------| -------|
| `staffTeamBasic`      | 5+ | 7+ |
| `staffTeamMedium`     | 7+ | 11+ |
| `staffTeamTop`        | 9+ | 16+ |
| `staffTeamSuper`      | 10  | 20  |
| Winner of contest     | 1 (bonus) | 2 (bonus) |

The precise number of points will depend how far your agent system is from these reference agents in the contest: the farther an agent is from the base reference agents, the more points it will attract. The only exception is `staffTeamSuper`, any team that finishes above it will earn full points (10 or 20).  -->

This together with the **quality of the Wiki and the Video** for the final submission will determine the points earned (20 points Wiki&Video + 10 points performance), then finally adjusted as per **individual contribution** and **SE quality practices** (see below) as needed. 
<!-- So, for example:
* To to reach a PASS level (25+ points out of 50 points), a submission must have a full marks Wiki&Video and an agent performing like `staffTeamBasic` in the final contest.  
* If an agent finishes between `staffTeamMedium` and `staffTeamTop` in the preliminary and final contest, and has a full marks Wiki&Video, then it will score between 38 (20 + 7+ 11) and 45 (20 + 9 + 16) points (the closer to `staffTeamTop`, the closer to 45). In a 10 scale, this is equivalent to a score between 7.6 and 9.0. -->

<!-- Overall, _assuming a full marks perfect Wiki report_, the `staffTeamBasic` corresponds to a just "pass" (50%), the `staffTeamMedium` to a H2, the `staffTeamTop` to an HD, and the `staffTeamSuper`  to a full mark 100% ninja Reversi agent. -->


### 4.2 Wiki

- **[10 marks]** A clear written description of the design decisions made, approaches taken, challenges experienced, and possible improvements. Do not describe generic algorithms, but tell us how you used them. Take a look at the template of the wiki.
-  **[5 marks]** An experimental section that justifies and explains the performance of the approaches implemented, including a table of results comparing the approaches implemented followed by a discussion.

### 4.3 Video

- **[2 marks]** A clear presentation of the design decisions made, challenges experienced, and possible improvements. 
- **[2 marks]** A clear demonstration and understanding of the subject material. 
- **[1 marks]** Demo of the different agents implemented across a variety of scenarios, showcasing pitfalls and benefits of each approach. No need of full game demo, just edit interesting parts and explain your insights.


### 4.4 Teamwork and Software Engineering professional practice

Besides the correctness and performance of your solutions, you must **follow good and professional SE practices**, including good use of git and professional communication during your development such as:

* _Commit early, commit often:_ single or few commits with all the solution or big chunks of it, is not good practice.
* _Use meaningful commit messages:_ as a comment in your code, the message should clearly summarize what the commit is about. Messages like "fix", "work", "commit", "changes" are poor and do not help us understand what was done.
* _Use atomic commits:_ avoid commits doing many things; let alone one commit solving many questions of the project. Each commit should be about one (little but interesting) thing. 
* _Use the Issue Tracker:_ use issues to keep track of tasks, enhancements, and bugs for your projects. They are also a great way to collaborate in a team, by assigning issues and discussing on them directly. Check GitHub [Mastering Issues Guide](https://guides.github.com/features/issues/).
* _Follow good workflow:_ use the standard branch-based development workflow, it will make your team much more productive and robust! Check GitHub [Workflow Guide](https://guides.github.com/introduction/flow/). 
* _Communicate in the GitHub Team:_ members of the group are expected to communicate, in an adequate and professional way, in the GitHub team created along the repo. For example, you could use GitHub team discussions, use issues and pull requests to track development status, or create project plans. Video and voice chats outside of GitHub are permissible (and encouraged), but text communication should be through the GitHub team where possible.

   [![How to work with github teams](img/teams.png)](https://www.loom.com/share/a1973a551a0142d5928ecab44d66ccaf)

* _Pair program_ if possible. You can use VScode and [this extension](https://docs.microsoft.com/en-us/visualstudio/liveshare/use/vscode) to liveshare your local code with your team members as guests. In pair programming, take turns at who's hosting the session (driving the coding) and who's observing. Alternatively, use any online platform to share your screen and program with your team members. Pair Programming is a widely used practice in industry. it is known to reduce errors, improve code quality, improve learning of all members, and reinforce the quality of the team's communication. See this entry about [pair programming](https://en.wikipedia.org/wiki/Pair_programming)

We will also inspect the **commit history** and **GitHub team** to check for high-quality SE practices and meaningful contributions of members. The results of this check can affect the overall mark of the project and point deductions may be applied when poor SE practices have been used along with uneven team members contributions (reported in the submission form). For example, few commits with a lot of code changes, or no or poor communication in the corresponding GitHub team may result in deductions, even if the performance is perfect. We need to make sure that you work as a team where everyone is contributing. This is a key skill in industry. “Effective teamwork begins and ends with communication.” — Mike Krzyzewski.


## 5. Important information

### How to create the Wiki

You can use the template given in [wiki-template/](wiki-template/) folder in order to create your wiki. Watch the video below.

[![Wiki](img/how_to_create_wiki.png)](https://www.loom.com/share/c434713d25b3478ebd2e924cd30a6f39)

### Corrections

From time to time, students or staff find errors (e.g., typos, unclear instructions, etc.) in the assignment specification. In that case, a corrected version of this file will be produced, announced, and distributed for you to commit and push into your repository (or following our instruction on ED if there is any updates). Because of that, you are NOT to modify this file in any way to avoid conflicts.

### Late submissions & extensions

Late submissions are truly inconvenient for this large assessment, as it involves other team members working for several weeks. Late submissions may not enter into the "official" contest and the team may then not receive feedback on time.  The project is available for 6 weeks, as a team, each member should plan and start early in order to minimize any unexpected circumstances near the end. Extensions will only be permitted in _exceptional_ circumstances; refer to [this question](https://docs.google.com/document/d/17YdTmDC54WHq0uZ-2UX3U8ESwULyBDJSD4SjKCrPXlA/edit?usp=sharing) in the course FAQs. Note that workload and/or heavy load of assignments will not be accepted as exceptional circumstances for an extension (we are not allowed to give any extension beyond Week 12 either). 

### About this repo

You must ALWAYS keep your fork **private** and **never share it** with anybody in or outside the course, except your teammates, _even after the course is completed_. You are not allowed to make another repository copy outside the provided GitHub Classroom without the written permission of the teaching staff.  

> **_Please do not distribute or post solutions to any of the projects._**

### Academic Dishonesty
 
**Academic Dishonesty:** This is an advanced course, so we expect full professionalism and ethical conduct.  Plagiarism is a serious issue. Please **don't let us down and risk our trust**. The staff take academic misconduct very seriously. Sophisticated _plagiarism detection_ software (e.g., [Codequiry](https://codequiry.com/), [Turinitin](https://www.turnitin.com/), etc.) will be used to check your code against other submissions in the class as well as resources available on the web for logical redundancy. These systems are really smart, so just do not risk it and keep professional. We trust you all to submit your own work only; please don't let us down. If you do, we will pursue the strongest consequences available to us according to the **University Academic Integrity policy**. For more information on this see file [Academic Integrity](ACADEMIC_INTEGRITY.md).


**We are here to help!:** We are here to help you! But we don't know you need help unless you tell us. We expect reasonable effort from you side, but if you get stuck or have doubts, please seek help. We will ran labs to support these projects, so use them! While you have to be careful to not post spoilers in the forum, you can always ask general questions about the techniques that are required to solve the projects. If in doubt whether a questions is appropriate, post a Private post to the instructors.

**Silence Policy:** A silence policy will take effect **48 hours** before this assignment is due. This means that no question about this assignment will be answered, whether it is asked on the newsgroup, by email, or in person. Use the last 48 hours to wrap up and finish your project quietly as well as possible if you have not done so already. Remember it is not mandatory to do all perfect, try to cover as much as possible. By having some silence we reduce anxiety, last minute mistakes, and unreasonable expectations on others. 


## 6. COMP90054 Code of Honour & Fair Play

We expect every UoM student taking this course to adhere to the **Code of Honour** under which every learner-student should:

* Submit their own original work.
* Do not share answers with others.
* Report suspected violations.
* Not engage in any other activities that will dishonestly improve their results or dishonestly improve or damage the results of others.

Being a contest, we expect **fair play** of all teams in this project. If you are in doubt of whether something would break the good spirit of the project, you must check with us early, not wait to be discovered. Any behaviour or code providing an unfair advantage or causing harm will be treated very seriously. We trust you, do not let us down and be a fair player.

Unethical behaviour is extremely serious and consequences are painful for everyone. We expect enrolled students/learners to take full **ownership** of your work and **respect** the work of teachers and other students.

## 7. Conclusion

This is the end of the project specification. 
> :loudspeaker: Remember to also read the [reversi.md](Reversi/reversi.md) file containing technical information that will come very useful.

If you still have doubts about the project and/or this specification do not hesitate asking in the [ED Discussion Forum](https://edstem.org/au/courses/6410/discussion/) and we will try to address it as quickly as we can!

**I very much hope you enjoy this final contest project and learn from it a lot**. 

**GOOD LUCK and HAPPY SPLENDOR!**

# reversi-contest-agent
