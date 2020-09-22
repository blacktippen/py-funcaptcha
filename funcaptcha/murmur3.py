__all__ = ['murmur3']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['x64Add', 'x64LeftShift', 'x64Multiply', 'x64Xor', 'x64hash128', 'x64Rotl', 'x64Fmix'])
@Js
def PyJs_anonymous_0_(m, n, this, arguments, var=var):
    var = Scope({'m':m, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'n', 'o'])
    var.put('m', Js([PyJsBshift(var.get('m').get('0'),Js(16.0)), (var.get('m').get('0')&Js(65535)), PyJsBshift(var.get('m').get('1'),Js(16.0)), (var.get('m').get('1')&Js(65535))]))
    var.put('n', Js([PyJsBshift(var.get('n').get('0'),Js(16.0)), (var.get('n').get('0')&Js(65535)), PyJsBshift(var.get('n').get('1'),Js(16.0)), (var.get('n').get('1')&Js(65535))]))
    var.put('o', Js([Js(0.0), Js(0.0), Js(0.0), Js(0.0)]))
    var.get('o').put('3', (var.get('m').get('3')+var.get('n').get('3')), '+')
    var.get('o').put('2', PyJsBshift(var.get('o').get('3'),Js(16.0)), '+')
    var.get('o').put('3', Js(65535), '&')
    var.get('o').put('2', (var.get('m').get('2')+var.get('n').get('2')), '+')
    var.get('o').put('1', PyJsBshift(var.get('o').get('2'),Js(16.0)), '+')
    var.get('o').put('2', Js(65535), '&')
    var.get('o').put('1', (var.get('m').get('1')+var.get('n').get('1')), '+')
    var.get('o').put('0', PyJsBshift(var.get('o').get('1'),Js(16.0)), '+')
    var.get('o').put('1', Js(65535), '&')
    var.get('o').put('0', (var.get('m').get('0')+var.get('n').get('0')), '+')
    var.get('o').put('0', Js(65535), '&')
    return Js([((var.get('o').get('0')<<Js(16.0))|var.get('o').get('1')), ((var.get('o').get('2')<<Js(16.0))|var.get('o').get('3'))])
PyJs_anonymous_0_._set_name('anonymous')
var.put('x64Add', PyJs_anonymous_0_)
@Js
def PyJs_anonymous_1_(m, n, this, arguments, var=var):
    var = Scope({'m':m, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'n', 'o'])
    var.put('m', Js([PyJsBshift(var.get('m').get('0'),Js(16.0)), (var.get('m').get('0')&Js(65535)), PyJsBshift(var.get('m').get('1'),Js(16.0)), (var.get('m').get('1')&Js(65535))]))
    var.put('n', Js([PyJsBshift(var.get('n').get('0'),Js(16.0)), (var.get('n').get('0')&Js(65535)), PyJsBshift(var.get('n').get('1'),Js(16.0)), (var.get('n').get('1')&Js(65535))]))
    var.put('o', Js([Js(0.0), Js(0.0), Js(0.0), Js(0.0)]))
    var.get('o').put('3', (var.get('m').get('3')*var.get('n').get('3')), '+')
    var.get('o').put('2', PyJsBshift(var.get('o').get('3'),Js(16.0)), '+')
    var.get('o').put('3', Js(65535), '&')
    var.get('o').put('2', (var.get('m').get('2')*var.get('n').get('3')), '+')
    var.get('o').put('1', PyJsBshift(var.get('o').get('2'),Js(16.0)), '+')
    var.get('o').put('2', Js(65535), '&')
    var.get('o').put('2', (var.get('m').get('3')*var.get('n').get('2')), '+')
    var.get('o').put('1', PyJsBshift(var.get('o').get('2'),Js(16.0)), '+')
    var.get('o').put('2', Js(65535), '&')
    var.get('o').put('1', (var.get('m').get('1')*var.get('n').get('3')), '+')
    var.get('o').put('0', PyJsBshift(var.get('o').get('1'),Js(16.0)), '+')
    var.get('o').put('1', Js(65535), '&')
    var.get('o').put('1', (var.get('m').get('2')*var.get('n').get('2')), '+')
    var.get('o').put('0', PyJsBshift(var.get('o').get('1'),Js(16.0)), '+')
    var.get('o').put('1', Js(65535), '&')
    var.get('o').put('1', (var.get('m').get('3')*var.get('n').get('1')), '+')
    var.get('o').put('0', PyJsBshift(var.get('o').get('1'),Js(16.0)), '+')
    var.get('o').put('1', Js(65535), '&')
    var.get('o').put('0', ((((var.get('m').get('0')*var.get('n').get('3'))+(var.get('m').get('1')*var.get('n').get('2')))+(var.get('m').get('2')*var.get('n').get('1')))+(var.get('m').get('3')*var.get('n').get('0'))), '+')
    var.get('o').put('0', Js(65535), '&')
    return Js([((var.get('o').get('0')<<Js(16.0))|var.get('o').get('1')), ((var.get('o').get('2')<<Js(16.0))|var.get('o').get('3'))])
PyJs_anonymous_1_._set_name('anonymous')
var.put('x64Multiply', PyJs_anonymous_1_)
@Js
def PyJs_anonymous_2_(m, n, this, arguments, var=var):
    var = Scope({'m':m, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'n'])
    var.put('n', Js(64.0), '%')
    if PyJsStrictEq(var.get('n'),Js(32.0)):
        return Js([var.get('m').get('1'), var.get('m').get('0')])
    else:
        if (var.get('n')<Js(32.0)):
            return Js([((var.get('m').get('0')<<var.get('n'))|PyJsBshift(var.get('m').get('1'),(Js(32.0)-var.get('n')))), ((var.get('m').get('1')<<var.get('n'))|PyJsBshift(var.get('m').get('0'),(Js(32.0)-var.get('n'))))])
        else:
            var.put('n', Js(32.0), '-')
            return Js([((var.get('m').get('1')<<var.get('n'))|PyJsBshift(var.get('m').get('0'),(Js(32.0)-var.get('n')))), ((var.get('m').get('0')<<var.get('n'))|PyJsBshift(var.get('m').get('1'),(Js(32.0)-var.get('n'))))])
PyJs_anonymous_2_._set_name('anonymous')
var.put('x64Rotl', PyJs_anonymous_2_)
@Js
def PyJs_anonymous_3_(m, n, this, arguments, var=var):
    var = Scope({'m':m, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'n'])
    var.put('n', Js(64.0), '%')
    if PyJsStrictEq(var.get('n'),Js(0.0)):
        return var.get('m')
    else:
        if (var.get('n')<Js(32.0)):
            return Js([((var.get('m').get('0')<<var.get('n'))|PyJsBshift(var.get('m').get('1'),(Js(32.0)-var.get('n')))), (var.get('m').get('1')<<var.get('n'))])
        else:
            return Js([(var.get('m').get('1')<<(var.get('n')-Js(32.0))), Js(0.0)])
PyJs_anonymous_3_._set_name('anonymous')
var.put('x64LeftShift', PyJs_anonymous_3_)
@Js
def PyJs_anonymous_4_(m, n, this, arguments, var=var):
    var = Scope({'m':m, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['m', 'n'])
    return Js([(var.get('m').get('0')^var.get('n').get('0')), (var.get('m').get('1')^var.get('n').get('1'))])
PyJs_anonymous_4_._set_name('anonymous')
var.put('x64Xor', PyJs_anonymous_4_)
@Js
def PyJs_anonymous_5_(h, this, arguments, var=var):
    var = Scope({'h':h, 'this':this, 'arguments':arguments}, var)
    var.registers(['h'])
    var.put('h', var.get('x64Xor')(var.get('h'), Js([Js(0.0), PyJsBshift(var.get('h').get('0'),Js(1.0))])))
    var.put('h', var.get('x64Multiply')(var.get('h'), Js([Js(4283543511), Js(3981806797)])))
    var.put('h', var.get('x64Xor')(var.get('h'), Js([Js(0.0), PyJsBshift(var.get('h').get('0'),Js(1.0))])))
    var.put('h', var.get('x64Multiply')(var.get('h'), Js([Js(3301882366), Js(444984403)])))
    var.put('h', var.get('x64Xor')(var.get('h'), Js([Js(0.0), PyJsBshift(var.get('h').get('0'),Js(1.0))])))
    return var.get('h')
PyJs_anonymous_5_._set_name('anonymous')
var.put('x64Fmix', PyJs_anonymous_5_)
@Js
def PyJs_anonymous_6_(key, seed, this, arguments, var=var):
    var = Scope({'key':key, 'seed':seed, 'this':this, 'arguments':arguments}, var)
    var.registers(['k2', 'c2', 'key', 'c1', 'bytes', 'seed', 'h1', 'remainder', 'h2', 'k1', 'i'])
    var.put('key', (var.get('key') or Js('')))
    var.put('seed', (var.get('seed') or Js(0.0)))
    var.put('remainder', (var.get('key').get('length')%Js(16.0)))
    var.put('bytes', (var.get('key').get('length')-var.get('remainder')))
    var.put('h1', Js([Js(0.0), var.get('seed')]))
    var.put('h2', Js([Js(0.0), var.get('seed')]))
    var.put('k1', Js([Js(0.0), Js(0.0)]))
    var.put('k2', Js([Js(0.0), Js(0.0)]))
    var.put('c1', Js([Js(2277735313), Js(289559509)]))
    var.put('c2', Js([Js(1291169091), Js(658871167)]))
    #for JS loop
    var.put('i', Js(0.0))
    while (var.get('i')<var.get('bytes')):
        try:
            def PyJs_LONG_7_(var=var):
                return var.put('k1', Js([((((var.get('key').callprop('charCodeAt', (var.get('i')+Js(4.0)))&Js(255))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(5.0)))&Js(255))<<Js(8.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(6.0)))&Js(255))<<Js(16.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(7.0)))&Js(255))<<Js(24.0))), ((((var.get('key').callprop('charCodeAt', var.get('i'))&Js(255))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(1.0)))&Js(255))<<Js(8.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(2.0)))&Js(255))<<Js(16.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(3.0)))&Js(255))<<Js(24.0)))]))
            PyJs_LONG_7_()
            def PyJs_LONG_8_(var=var):
                return var.put('k2', Js([((((var.get('key').callprop('charCodeAt', (var.get('i')+Js(12.0)))&Js(255))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(13.0)))&Js(255))<<Js(8.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(14.0)))&Js(255))<<Js(16.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(15.0)))&Js(255))<<Js(24.0))), ((((var.get('key').callprop('charCodeAt', (var.get('i')+Js(8.0)))&Js(255))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(9.0)))&Js(255))<<Js(8.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(10.0)))&Js(255))<<Js(16.0)))|((var.get('key').callprop('charCodeAt', (var.get('i')+Js(11.0)))&Js(255))<<Js(24.0)))]))
            PyJs_LONG_8_()
            var.put('k1', var.get('x64Multiply')(var.get('k1'), var.get('c1')))
            var.put('k1', var.get('x64Rotl')(var.get('k1'), Js(31.0)))
            var.put('k1', var.get('x64Multiply')(var.get('k1'), var.get('c2')))
            var.put('h1', var.get('x64Xor')(var.get('h1'), var.get('k1')))
            var.put('h1', var.get('x64Rotl')(var.get('h1'), Js(27.0)))
            var.put('h1', var.get('x64Add')(var.get('h1'), var.get('h2')))
            var.put('h1', var.get('x64Add')(var.get('x64Multiply')(var.get('h1'), Js([Js(0.0), Js(5.0)])), Js([Js(0.0), Js(1390208809)])))
            var.put('k2', var.get('x64Multiply')(var.get('k2'), var.get('c2')))
            var.put('k2', var.get('x64Rotl')(var.get('k2'), Js(33.0)))
            var.put('k2', var.get('x64Multiply')(var.get('k2'), var.get('c1')))
            var.put('h2', var.get('x64Xor')(var.get('h2'), var.get('k2')))
            var.put('h2', var.get('x64Rotl')(var.get('h2'), Js(31.0)))
            var.put('h2', var.get('x64Add')(var.get('h2'), var.get('h1')))
            var.put('h2', var.get('x64Add')(var.get('x64Multiply')(var.get('h2'), Js([Js(0.0), Js(5.0)])), Js([Js(0.0), Js(944331445)])))
        finally:
                var.put('i', (var.get('i')+Js(16.0)))
    var.put('k1', Js([Js(0.0), Js(0.0)]))
    var.put('k2', Js([Js(0.0), Js(0.0)]))
    while 1:
        SWITCHED = False
        CONDITION = (var.get('remainder'))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(15.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(14.0)))]), Js(48.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(14.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(13.0)))]), Js(40.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(13.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(12.0)))]), Js(32.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(12.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(11.0)))]), Js(24.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(11.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(10.0)))]), Js(16.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(10.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(9.0)))]), Js(8.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(9.0)):
            SWITCHED = True
            var.put('k2', var.get('x64Xor')(var.get('k2'), Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(8.0)))])))
            var.put('k2', var.get('x64Multiply')(var.get('k2'), var.get('c2')))
            var.put('k2', var.get('x64Rotl')(var.get('k2'), Js(33.0)))
            var.put('k2', var.get('x64Multiply')(var.get('k2'), var.get('c1')))
            var.put('h2', var.get('x64Xor')(var.get('h2'), var.get('k2')))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(8.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(7.0)))]), Js(56.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(7.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(6.0)))]), Js(48.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(6.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(5.0)))]), Js(40.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(5.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(4.0)))]), Js(32.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(4.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(3.0)))]), Js(24.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(3.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(2.0)))]), Js(16.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(2.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), var.get('x64LeftShift')(Js([Js(0.0), var.get('key').callprop('charCodeAt', (var.get('i')+Js(1.0)))]), Js(8.0))))
        if SWITCHED or PyJsStrictEq(CONDITION, Js(1.0)):
            SWITCHED = True
            var.put('k1', var.get('x64Xor')(var.get('k1'), Js([Js(0.0), var.get('key').callprop('charCodeAt', var.get('i'))])))
            var.put('k1', var.get('x64Multiply')(var.get('k1'), var.get('c1')))
            var.put('k1', var.get('x64Rotl')(var.get('k1'), Js(31.0)))
            var.put('k1', var.get('x64Multiply')(var.get('k1'), var.get('c2')))
            var.put('h1', var.get('x64Xor')(var.get('h1'), var.get('k1')))
        SWITCHED = True
        break
    var.put('h1', var.get('x64Xor')(var.get('h1'), Js([Js(0.0), var.get('key').get('length')])))
    var.put('h2', var.get('x64Xor')(var.get('h2'), Js([Js(0.0), var.get('key').get('length')])))
    var.put('h1', var.get('x64Add')(var.get('h1'), var.get('h2')))
    var.put('h2', var.get('x64Add')(var.get('h2'), var.get('h1')))
    var.put('h1', var.get('x64Fmix')(var.get('h1')))
    var.put('h2', var.get('x64Fmix')(var.get('h2')))
    var.put('h1', var.get('x64Add')(var.get('h1'), var.get('h2')))
    var.put('h2', var.get('x64Add')(var.get('h2'), var.get('h1')))
    def PyJs_LONG_9_(var=var):
        return ((((Js('00000000')+PyJsBshift(var.get('h1').get('0'),Js(0.0)).callprop('toString', Js(16.0))).callprop('slice', (-Js(8.0)))+(Js('00000000')+PyJsBshift(var.get('h1').get('1'),Js(0.0)).callprop('toString', Js(16.0))).callprop('slice', (-Js(8.0))))+(Js('00000000')+PyJsBshift(var.get('h2').get('0'),Js(0.0)).callprop('toString', Js(16.0))).callprop('slice', (-Js(8.0))))+(Js('00000000')+PyJsBshift(var.get('h2').get('1'),Js(0.0)).callprop('toString', Js(16.0))).callprop('slice', (-Js(8.0))))
    return PyJs_LONG_9_()
PyJs_anonymous_6_._set_name('anonymous')
var.put('x64hash128', PyJs_anonymous_6_)


# Add lib to the module scope
murmur3 = var.to_python()