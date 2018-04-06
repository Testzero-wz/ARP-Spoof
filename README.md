---
date: 2018-03-16 15:52
status: public
title: README
---

# Tk-for-CQU-Course
An simple,humble GUI program for CQU, base on Python Tkinter

# Usage
 Input your student ID number & password into the entry, select what kind of courses you want(Defult is major course) and click ** Login Button **

![](~/15-55-25.jpg)

+ If you got an error when you Login, make sure your what you input are both correct and try again.
+ If the program no responese after you click **Login Button**, perhaps  our CQU teaching administration system were busy, plz wait a moment.

If your ID & password are correct, the seceond window will show up
(Like this)

![](~/15-57-30.jpg)
Left box is about lesson list while right side box will contain the course detailed information you choose on the left side.

When you double click on the item which is no about course(Like first, second item), it will be a notice on the right window  

![](~/16-15-50.jpg)

Of course, there are some notes when the crawler thread didn't get info from servers .

![](~/16-59-02.jpg)


You can select an item on the right side and it will be selected into **selected widget** which on the bottom of window

![](~/16-36-45.jpg)

At most,   only three courses can be selected and you can click the **Clear Button** remove all you selected.
The refresh button offer a function which you can refresh  the course info by hand, but  I **highly recommend**  not using this feature when it is not necessary, it may cause a servere network congestion which is not good for you and other students .

Finally, click the **Submit Button** and the courses you selected will send to the server,  then it will automatically refresh once , you needn't refresh again .

![](~/17-09-07.jpg)


## Tips
**There are no some alert or notice message when your  requests are successfully handled by servers or not .
The only thing you can do is to wait for the message box on the left to update.
Ahahahahah**









