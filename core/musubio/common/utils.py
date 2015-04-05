
def console(message):
    border = ('*' * ((len(message) / len('*') + 4) + 1))[:len(message) + 4]
    print '\n%s' % border
    print '* %s *' % message
    print '%s\n' % border