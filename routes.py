# coding: utf-8

routes = list()
#from handlers import user, jwxt, sport, laf


#routes.append((r'/login.json', user.LoginHandler))
#routes.append((r'/logout.json', user.LogoutHandler))

#routes.append((r'/user/jwxt/course_table.json', jwxt.CourseTableHandler))
#routes.append((r'/user/jwxt/grade.json', jwxt.GradeHandler))

#routes.append((r'/user/sport/score.json', sport.ScoreHandler))

#routes.append((r'/laf/lost.json', laf.GetLostHandler))

from handlers import index, api

routes.append((r'/', index.IndexHandler))
routes.append((r'/login', index.LoginHandler))
routes.append((r'/logout', index.LogoutHandler))
routes.append((r'/user', index.UserHandler))
routes.append((r'/user/coursetable', index.CourseHandler))
routes.append((r'/user/grade', index.GradeHandler))
routes.append((r'/user/daka', index.DakaHandler))
routes.append((r'/user/main_news', index.MainNewsHandler))
routes.append((r'/user/public_news', index.PublicNewsHandler))
routes.append((r'/user/cet', index.CETHandler))
routes.append((r'/user/eat', index.EatHandler))

# API
routes.append((r'/api/login', api.LoginHandler))
routes.append((r'/api/logout', api.LogoutHandler))
routes.append((r'/api/course_table', api.CourseTableHandler))
