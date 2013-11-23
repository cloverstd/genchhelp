# coding: utf-8

routes = list()
#from handlers import user, jwxt, sport, laf


#routes.append((r'/login.json', user.LoginHandler))
#routes.append((r'/logout.json', user.LogoutHandler))

#routes.append((r'/user/jwxt/course_table.json', jwxt.CourseTableHandler))
#routes.append((r'/user/jwxt/grade.json', jwxt.GradeHandler))

#routes.append((r'/user/sport/score.json', sport.ScoreHandler))

#routes.append((r'/laf/lost.json', laf.GetLostHandler))

from handlers import mobile, api, desktop


# Mobile
routes.append((r'/', mobile.IndexHandler))
routes.append((r'/login', mobile.LoginHandler))
routes.append((r'/logout', mobile.LogoutHandler))
routes.append((r'/user', mobile.UserHandler))
routes.append((r'/user/coursetable', mobile.CourseHandler))
routes.append((r'/user/grade', mobile.GradeHandler))
routes.append((r'/user/daka', mobile.DakaHandler))
routes.append((r'/user/main_news', mobile.MainNewsHandler))
routes.append((r'/user/public_news', mobile.PublicNewsHandler))
routes.append((r'/user/cet', mobile.CETHandler))
routes.append((r'/user/eat', mobile.EatHandler))
routes.append((r'/user/credit', mobile.CreditHandler))

# Desktop
routes.append((r'/d', desktop.IndexHandler))
routes.append((r'/d/', desktop.IndexHandler))
routes.append((r'/d/cet', desktop.CETHandler))
routes.append((r'/d/sport', desktop.DakaHandler))
routes.append((r'/d/comment', desktop.CommentHandler))
routes.append((r'/d/about', desktop.AboutHandler))

# API
routes.append((r'/api/login', api.LoginHandler))
routes.append((r'/api/logout', api.LogoutHandler))
routes.append((r'/api/course', api.CourseHandler))  # 课表
routes.append((r'/api/grade/(\d{4})/(\d{4})/([12])', api.GradeHandler))  # 成绩
routes.append((r'/api/daka/(\d+)/(\d{8})', api.DakaHandler))  # 打卡
routes.append((r'/api/credit/(\d{4})/(\d{4})/([12])', api.CreditHandler))  # 素质拓展
routes.append((r'/api/cet', api.CETHandler))  # 四六级
routes.append((r'/api/news/main', api.MainNewsHandler))  # 建桥要闻
routes.append((r'/api/news/public', api.PublicNewsHandler))  # 信息公开
