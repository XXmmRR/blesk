not_anon_risk = 'Спасибо за Вашу бдительность❤️. Ваше обращение будет обработано модератором, после чего мы дадим вам обратную связь по решению ситуации.👌'
not_anon_solve_problem = 'Благодарим Вас за участие в жизни "блеска"🤗, ваше обращение будет обработано модератором, после чего мы дадим вам обратную связь по предложенному решению!'
not_anon_idea = 'Спасибо за Вашу идею 💡 . Модератор обработает ваше обращение, идея будет доведена до ответственных сотрудников. 👌После чего мы дадим вам обратную связь по возможности ее реализации😊'
not_anon_help = 'Благодарим вас за доверие.❤️Модератор обработает ваш запрос и мы вернемся к Вам с обратной связью🤗.'
not_anon_reward = 'Спасибо, что замечаете позитив вокруг. 🤗Ваша благодарность будет передана адресату.❤️'
anon_risk = 'Спасибо за Вашу бдительность🧐. Ваш запрос будет обработан модератором и предложено решение ситуации.🫡'
anon_solve_problem = 'Благодарим за Ваше участие в жизни "блеска"❤️, Ваше обращение будет обработано модератором, после чего предложено решение проблемы 👌'
anon_idea = 'Спасибо за Вашу идею💡 и стремление сделать "блеск" лучше🥰. Модератор обработает Ваше обращение, идея будет доведена до ответственных сотрудников🤗.'
anon_reward = 'Спасибо, что замечаете позитив вокруг. 🤗Ваша благодарность будет передана адресату.❤️'

text_dict = {'Предупредить о риске❗️': {True: anon_risk, False: not_anon_risk, 'Запрос': 'Подробно опишите суть Вашего обращения. Если информация касается конкретного филиала, укажите адрес.'}, 
             'Рассказать о проблеме😱': {True: anon_solve_problem, False: not_anon_solve_problem, 'Запрос': 'Пожалуйста, подробно опишите суть проблемы, с которой вы столкнулись. Если видите варианты решения, укажите их. Если информация касается конкретного филиала, укажите адрес'},
             'Предложить идею💡': {True: anon_idea, False: not_anon_idea, 'Запрос': 'Опишите, пожалуйста, подробно свою идею. Какие проблемы может решить или какие потребности может закрыть ? Если идея касается конкретного филиала, укажите адрес'},
             'Попросить о помощи🙏🏻': {False: not_anon_help, "Запрос": 'Опишите ваш запрос'},
             'Поблагодарить кого-то❤️': {True: anon_reward, False: not_anon_reward, 'Запрос': 'Опишите, пожалуйста, подробно кого и за что хотели бы поблагодарить'}
             }  