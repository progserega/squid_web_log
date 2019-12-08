#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import os
import time
import re
import sys
import config as conf
import logging
from logging import handlers
from file_read_backwards import FileReadBackwards

log=None

def main():
  global log

  filter_string=None
  if conf.debug:
    web_user_name = "DEBUG script in console"
    web_user_agent = "console"
    web_user_addr = "127.0.0.1"
    web_user_host = "localhost"

  else:
    form = cgi.FieldStorage()

    web_user_agent=os.getenv("HTTP_USER_AGENT")
    web_user_addr=os.getenv("REMOTE_ADDR")
    web_user_host=os.getenv("REMOTE_HOST")
    web_user_name=os.getenv('AUTHENTICATE_SAMACCOUNTNAME')

    print_html_header()

    # Поле 'work_sites_regex' содержит не пустое значение:
    if 'filter_string' in form:
      filter_string = "%s" % cgi.escape(form['filter_string'].value)

  log.info("%s, %s, %s, %s - try find %s" % (web_user_addr,web_user_host,web_user_agent,web_user_name,filter_string) )

  index=0
  result=[]
  with FileReadBackwards(conf.access_log_path, encoding="utf-8") as frb:
    for l in frb:
      if filter_string!=None and filter_string not in l:
        continue
      l=re.sub('\s+',' ', l)
      if conf.debug:
        out(l)
      item={}
      words=l.split(' ')
      item["unixtime"] =float(words[0])
      item["string_time"] =time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(item["unixtime"]))
      item["download_time_ms"] =words[1]
      if item["download_time_ms"].isdigit():
        item["download_time_ms"] = float(item["download_time_ms"])
      else:
        item["download_time_ms"]=0
      item["download_time_sec"] =item["download_time_ms"]/1000
      item["clinet_address"] =words[2]
      item["result_code"] =words[3]
      item["downloaded_bytes"] =int(words[4])
      item["get_method"] =words[5]
      item["url"]=words[6]
      item["login"]=words[7]
      if 9 in words:
        item["data_type"]==words[9]
      else:
        item["data_type"]=""

      result.append(item)

      index+=1
      if index > conf.result_count:
        break

  if conf.debug!=True:
    print_html_result(result,filter_string)
    out("</body></html>")
  return True

def print_html_header():
  out("""
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<HTML>
<HEAD>
<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=utf-8">
<TITLE>Логи сквида</TITLE>
<META NAME="GENERATOR" CONTENT="OpenOffice.org 3.1  (Linux)">
<META NAME="AUTHOR" CONTENT="Сергей Семёнов">
<META NAME="CREATED" CONTENT="20100319;10431100">
<META NAME="CHANGEDBY" CONTENT="Сергей Семёнов">
<META NAME="CHANGED" CONTENT="20100319;10441400">

<style type="text/css">
tr:nth-child(even) {background: #DDD}
tr:nth-child(odd) {background: #FFF}
tr	{
	text-align:center;
	font-size: 0.835vw; //around 14px at 1920px
}
#url {
	text-align:left;
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}	
#access_good {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
  background: green;
	color: #000000;
}	
#access_fail {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	background: red;
	color: #000000;
}	
#http_error {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	background: magenta;
	color: #000000;
}	
#cnt {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}	
#username {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#acc {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#pwd {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#desc {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#acc_drsk_email {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#pwd_drsk_email {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#acc_rsprim_email {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#pwd_rsprim_email {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#acc_status {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#hostname {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#cellphone {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#position {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#department {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#host_ip {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#host_os {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#host_os_ver {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#patches {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#creator_ip {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#created_time {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
#creator_who {
	border: 1px solid #8da1b5;
	font-family: Tahoma;
	color: #4f4f4f;
}
   .banned {
    color: red; /* Красный цвет выделения */
   }
   .selected_node {
    color: green; /* Зелёный цвет выделения */
  background: #D9FFAD;
  font-size: 150%;
   }
</style>

</HEAD>
<BODY LANG="ru-RU" LINK="#000080" VLINK="#800000" DIR="LTR">
""")


def out(msg):
  sys.stdout.buffer.write(msg.encode('utf8'))
  sys.stdout.flush()

def print_html_result(result, filter_string):

  if filter_string == None:
    filter_postfix=" - без фильтра"
  else:
    filter_postfix=", отфильтрованного по строке: %s"%filter_string
  out("""
    <TABLE BORDER>
    <TR>    
        <TH COLSPAN=9>Отчёт сквида (%d строк)%s (последние строки сверху)</TH>
    </TR>
    <TR>    
        <TH COLSPAN=9>Красный - ошибка сквида, фиолетовый - ошибка сайта в интернете, зелёный - всё хорошо</TH>
    </TR>
    <TR>
        <TH COLSPAN=1>Дата/время запроса</TH>
        <TH COLSPAN=1>Результат http (результат сквида)</TH>
        <TH COLSPAN=1>ссылка</TH>
        <TH COLSPAN=1>доменная авторизация</TH>
        <TH COLSPAN=1>адрес клиента</TH>
        <TH COLSPAN=1>скачано байт</TH>
        <TH COLSPAN=1>скачано за время (сек)</TH>
        <TH COLSPAN=1>метод запроса</TH>
    </TR>
    """%(conf.result_count,filter_postfix))

  for item in result:

    access_result_source=item["result_code"]
    access_result_string=access_result_source
    access_result_css="http_error"

    if "100" in access_result_source:
      access_result_string="продолжай"
      access_result_css="access_good"
    elif "101" in access_result_source:
      access_result_string="переключение протоколов"
      access_result_css="access_good"
    elif "102" in access_result_source:
      access_result_string="идёт обработка"
      access_result_css="access_good"
    elif "200" in access_result_source:
      access_result_string="успешно скачан"
      access_result_css="access_good"
    elif "201" in access_result_source:
      access_result_string="создано"
      access_result_css="access_good"
    elif "202" in access_result_source:
      access_result_string="принято"
      access_result_css="access_good"
    elif "203" in access_result_source:
      access_result_string="информация не авторитетна"
    elif "204" in access_result_source:
      access_result_string="нет содержимого"
    elif "205" in access_result_source:
      access_result_string="сбросить содержимое"
    elif "206" in access_result_source:
      access_result_string="частичное содержимо"
      access_result_css="access_good"
    elif "207" in access_result_source:
      access_result_string="многостатусный"
    elif "208" in access_result_source:
      access_result_string="уже сообщалось"
      access_result_css="access_good"
    elif "226" in access_result_source:
      access_result_string="использовано IM"
      access_result_css="access_good"
    elif "300" in access_result_source:
      access_result_string="множество выборов"
      access_result_css="access_good"
    elif "301" in access_result_source:
     access_result_string="перемещено навсегда"
    elif "302" in access_result_source:
     access_result_string="перемещено временно"
    elif "302" in access_result_source:
      access_result_string="найдено"
      access_result_css="access_good"
    elif "303" in access_result_source:
     access_result_string="смотреть другое"
    elif "304" in access_result_source:
      access_result_string="не изменялось"
      access_result_css="access_good"
    elif "305" in access_result_source:
     access_result_string="использовать прокси"
    elif "307" in access_result_source:
      access_result_string="временное перенаправление"
      access_result_css="access_good"
    elif "308" in access_result_source:
      access_result_string="постоянное перенаправление"
      access_result_css="access_good"
    elif "400" in access_result_source:
     access_result_string="плохой, неверный запрос"
    elif "401" in access_result_source:
     access_result_string="не авторизован (не представился)"
    elif "402" in access_result_source:
     access_result_string="необходима оплата"
    elif "403" in access_result_source:
     access_result_string="запрещено (не уполномочен)"
    elif "404" in access_result_source:
     access_result_string="не найдено"
    elif "405" in access_result_source:
     access_result_string="метод не поддерживается"
    elif "406" in access_result_source:
     access_result_string="неприемлемо"
    elif "407" in access_result_source:
     access_result_string="необходима аутентификация прокси"
     access_result_css="access_fail"
    elif "408" in access_result_source:
     access_result_string="истекло время ожидания"
    elif "409" in access_result_source:
     access_result_string="конфликт"
    elif "410" in access_result_source:
     access_result_string="удалён"
    elif "411" in access_result_source:
     access_result_string="необходима длина"
    elif "412" in access_result_source:
     access_result_string="условие ложно"
    elif "413" in access_result_source:
     access_result_string="полезная нагрузка слишком велика"
    elif "414" in access_result_source:
     access_result_string="URI слишком длинный"
    elif "415" in access_result_source:
     access_result_string="неподдерживаемый тип данных"
    elif "416" in access_result_source:
     access_result_string="диапазон не достижим"
    elif "417" in access_result_source:
     access_result_string="ожидание не удалось"
    elif "418" in access_result_source:
     access_result_string="я — чайник"
    elif "419" in access_result_source:
     access_result_string="обычно ошибка проверки CSRF"
    elif "422" in access_result_source:
     access_result_string="Misdirected Request"
    elif "422" in access_result_source:
     access_result_string="необрабатываемый экземпляр"
    elif "423" in access_result_source:
     access_result_string="заблокировано"
    elif "424" in access_result_source:
     access_result_string="невыполненная зависимость"
    elif "426" in access_result_source:
     access_result_string="необходимо обновление"
    elif "428" in access_result_source:
     access_result_string="необходимо предусловие"
    elif "429" in access_result_source:
     access_result_string="слишком много запросов"
    elif "431" in access_result_source:
     access_result_string="поля заголовка запроса слишком большие"
    elif "449" in access_result_source:
     access_result_string="повторить с"
    elif "451" in access_result_source:
     access_result_string="недоступно по юридическим причинам"
    elif "499" in access_result_source:
     access_result_string="клиент закрыл соединение"
    elif "500" in access_result_source:
     access_result_string="внутренняя ошибка сервера"
    elif "501" in access_result_source:
     access_result_string="не реализовано"
    elif "502" in access_result_source:
     access_result_string="плохой, ошибочный шлюз"
    elif "503" in access_result_source:
     access_result_string="сервис недоступен"
    elif "504" in access_result_source:
     access_result_string="шлюз не отвечает"
    elif "505" in access_result_source:
     access_result_string="версия HTTP не поддерживается"
    elif "506" in access_result_source:
     access_result_string="вариант тоже проводит согласование"
    elif "507" in access_result_source:
     access_result_string="переполнение хранилища"
    elif "508" in access_result_source:
     access_result_string="обнаружено бесконечное перенаправление"
    elif "509" in access_result_source:
     access_result_string="исчерпана пропускная ширина канала"
    elif "510" in access_result_source:
     access_result_string="не расширено"
    elif "511" in access_result_source:
     access_result_string="требуется сетевая аутентификация"
    elif "520" in access_result_source:
     access_result_string="неизвестная ошибка"
    elif "521" in access_result_source:
     access_result_string="веб-сервер не работает"
    elif "522" in access_result_source:
     access_result_string="соединение не отвечает"
    elif "523" in access_result_source:
     access_result_string="источник недоступен"
    elif "524" in access_result_source:
     access_result_string="время ожидания истекло"
    elif "525" in access_result_source:
     access_result_string="квитирование SSL не удалось"
    elif "526" in access_result_source:
     access_result_string="недействительный сертификат SSL"

    if "TCP_MISS" in access_result_source:
      access_result_string+=" / Запрошенного объекта не было в кеше"
    elif "TCP_HIT" in access_result_source:
      access_result_string+=" / Верная копия запрошенного объекта была в кеше"
    elif "TCP_REFRESH_HIT" in access_result_source:
      access_result_string+=" / Запрошенный объект был закеширован, но УСТАРЕЛ"
    elif "TCP_REF_FAIL_HIT" in access_result_source:
      access_result_string+=" / Запрошенный объект был закеширован, но УСТАРЕЛ"
    elif "TCP_REFRESH_MISS" in access_result_source:
      access_result_string+=" / Запрошенный объект был закеширован, но УСТАРЕЛ"
    elif "TCP_CLIENT_REFRESH_MISS" in access_result_source:
      access_result_string+=" / The client issued a \"no-cache\" pragma, or some analogous cache control command along with the request. Thus, the cache has to refetch the object."
    elif "TCP_IMS_HIT" in access_result_source:
      access_result_string+=" / Клиент использовал IMS-запрос для объекта, который был найден в кеше свежим."
    elif "TCP_SWAPFAIL_MISS" in access_result_source:
      access_result_string+=" / Объект скорее всего был в кеше, но доступа к нему нет"
    elif "TCP_NEGATIVE_HIT" in access_result_source:
      access_result_string+=" / Запрос для негативно кешированных объектов типа \"404 not found\""
    elif "TCP_MEM_HIT" in access_result_source:
      access_result_string+=" / Верная копия запрошенного объекта была в кеше и в памяти, доступа к диске не производилось"
    elif "TCP_DENIED" in access_result_source:
      access_result_string+=" / Доступ запрещен для этого запроса"
      access_result_css="access_fail"
    elif "TCP_OFFLINE_HIT" in access_result_source:
      access_result_string+=" / The requested object was retrieved from the cache during offline mode"
    elif "UDP_HIT" in access_result_source:
      access_result_string+=" / Верная копия запрошенного объекта была в кеше"
    elif "UDP_MISS" in access_result_source:
      access_result_string+=" / Запрошенный объект отсутствует в этом кеше"
    elif "UDP_DENIED" in access_result_source:
      access_result_string+=" / Доступ запрещен для этого запроса"
      access_result_css="access_fail"
    elif "UDP_INVALID" in access_result_source:
      access_result_string+=" / Был получен неверный запрос"
    elif "UDP_MISS_NOFETCH" in access_result_source:
      access_result_string+=" / During \"-Y\" startup, or during frequent failures, a cache in hit only mode will return either UDP_HIT or this code. Neighbours will thus only fetch hits"
    elif "NONE" in access_result_source:
      access_result_string+=" / Seen with errors and cachemgr requests"
    else:
      access_result_string+=" (%s)"%access_result_source
      

    downloaded_bytes=item["downloaded_bytes"]
    result_downloaded=downloaded_bytes
    result_downloaded_tmp=downloaded_bytes
    download_postfix="байт"
    result_downloaded_tmp=result_downloaded_tmp/1024
    if result_downloaded_tmp > 1:
      download_postfix="Кб"
      result_downloaded=result_downloaded_tmp
    result_downloaded_tmp=result_downloaded_tmp/1024
    if result_downloaded_tmp > 1:
      download_postfix="Мб"
      result_downloaded=result_downloaded_tmp
    result_downloaded_tmp=result_downloaded_tmp/1024
    if result_downloaded_tmp > 1:
      download_postfix="Гб"
      result_downloaded=result_downloaded_tmp
    downloaded_string="%.0f %s"%(result_downloaded,download_postfix)

    if item["login"] == "-":
      login_css="access_fail"
    else:
      login_css="access_good"
      
    out("""<TR>
     <TD id="username">%(string_time)s</TD>
     <TD id="%(access_result_css)s">%(access_result_string)s</TD>
     <TD id="url">%(url)s</TD>
     <TD id="%(login_css)s">%(login)s</TD>
     <TD id="desc">%(clinet_address)s</TD>
     <TD id="acc_drsk_email">%(downloaded_string)s</TD>
     <TD id="pwd_drsk_email">%(download_time_sec)s сек.</TD>
     <TD id="acc_rsprim_email">%(get_method)s</TD>
     </TR>""" % {\
     "string_time":item["string_time"], \
     "url":item["url"], \
     "clinet_address":item["clinet_address"], \
     "downloaded_string":downloaded_string, \
     "download_time_sec":item["download_time_sec"], \
     "access_result_css":access_result_css, \
     "access_result_string":access_result_string, \
     "login":item["login"], \
     "login_css":login_css, \
     "access_result_source":access_result_source, \
     "get_method":item["get_method"] \
     })
  out("</TABLE>")



if __name__ == '__main__':
  log=logging.getLogger("squid_log")
  if conf.debug:
    log.setLevel(logging.DEBUG)
  else:
    log.setLevel(logging.INFO)

  # create the logging file handler
  #fh = logging.FileHandler(conf.log_path)
  fh = logging.handlers.TimedRotatingFileHandler(conf.log_path, when=conf.log_backup_when, backupCount=conf.log_backup_count, encoding='utf-8')
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s:%(lineno)d - %(funcName)s() %(levelname)s - %(message)s')
  fh.setFormatter(formatter)

  # add handler to logger object
  log.addHandler(fh)

  log.info("Program started")

  log.info("python version=%s"%sys.version)

  if main()==False:
    log.error("error main()")
    sys.exit(1)
  log.info("Program exit!")
