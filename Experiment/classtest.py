class testclass(object):
    """ My little class experiment """
    classvar1 = "Wat"
    classvar2 = "this"
    def __init__(self,passedvar):
        print "inside the init thing"
        self.var = "idk"
        self.var1 = passedvar
        print passedvar
        
    def bleh(self):
        print self.var
        self.var = "something else"
        print self.var


test = testclass("passing this string")
test.bleh()
test.classvar1
test.classvar2
print test.var
print test.var1


class MyStuff(object):
    def __init__(self):
        self.tangerine = "And now a thousand years between"
    def apple(self):
        print "I AM CLASSY APPLES!"
        
        
class Song(object):
    def __init__(self, lyrics):
        self.lyrics = lyrics
    def sing_me_a_song(self):
        for line in self.lyrics:
            print line

happy_bday = Song(["Happy birthday to you",
                   "I don't want to get sued",
                   "So I'll stop right there"])

bulls_on_parade = Song(["They rally around tha family",
                        "With pockets full of shells"])
