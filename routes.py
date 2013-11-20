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
routes.append((r'/api/course_table', api.CourseTableHandler))
routes.append((r'/api/cet', api.CETHandler))
routes.append((r'/api/test', api.TESTHandler))
