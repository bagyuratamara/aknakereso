# Aknakereső

A projectem egy egy aknakereső játékot tartalmaz egy egyszerű deep learning modullal.


Az aknakereső egy logikai játék, amelynek a célja, hogy egy táblát feledjünk anélkül, hogy egy bombába ütköznénk.

## A futtatáshoz szükséges modulok:
    - Pytorch
    - Pygame

## Program indítása
    - A programot a runner.py fájlal lehet elindítani, amely egy kezdőlapot fog mutatni
    - Itt lehet választani, hogy mi szerettnénk játszani, vagy a gép játsszon
![Reference Image](/assets/1.png)

## Játék leírás
A játék kódja az aknakereső.py-ban látható.

### Játékszabályok

    - cellákat felfedni bal egérkattintással lehet
    - bombákat jelölni jobb egérkattintással lehet
    - a biztonságos mezőkön számokat láthatnunk, melyek azt jelzik, hány bomba van a szomszédos cellában
    - a játéknak akkor van vége, ha az összes üres cellát felfedtük, vagy egy bombára kattintottunk
    - a játék tetején láthatjuk a nem jelölt bombák számát
    - a zöld gombbal lehet kilépni a játékból és visszatérni a főoldalra

![Reference Image](/assets/2.png) ![Reference Image](/assets/3.png)

## Deep learning modul

Egy nagyon egyszerű modellt hoztam létre, amely megtanulja kezelni a játék felületét, PyTorch segítségével.

MIvel az eredeti játékom teljesen a pygame-en épült, itt teljesen át kellett alakítanom a kódot, ami a aknakereso_bot.py-ban látható.

Egy DQN modellt alkalmaztam, ami a DQN_model-ben megtekinthető.

Az agent.py-ban látható agent működését, aki az aknakereső játék során az epsilon-csökkenési stratégiát alkalmazva, valamint a jutalmak és büntetések alapján dönt a lehetséges lépések között.

### Pontrendszer:

    - győzelem: +15 pont
    - bombára helyezett jelölés: +1 pont
    - bombáról levett jelölés: -1 pont
    - random lépés (egy szomszédos cella sincs felfedve): -1 pont
    - vereség: -annyi pont, ahány nem jelölt bomba maradt
    - egyéb lépés: 0 pont




    
