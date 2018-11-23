var GetGuid = function (m, n) {
    var o = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'.split('');
    var p = [], q;
    n = n || o.length;
    if (m) {
        for (q = 0; q < m; q++)
            p[q] = o[0 | Math.random() * n]
    } else {
        var r;
        p[8] = p[13] = p[18] = p[23] = '-';
        p[14] = '4';
        for (q = 0; q < 36; q++) {
            if (!p[q]) {
                r = 0 | Math.random() * 16;
                p[q] = o[(q == 19) ? (r & 0x3) | 0x8 : r]
            }
        }
    }
    ;
    return p.join('')
};

var DoTk = function (n1,o1) {
    var n = n1,
        o = o1;
    return eval(function (p, q, r, s, e, t) {
        e = function (u) {
            return (u < q ? "" : e(parseInt(u / q))) + ((u = u % q) > 35 ? String.fromCharCode(u + 29) : u.toString(36))
        }
        ;
        if (!''.replace(/^/, String)) {
            while (r--)
                t[e(r)] = s[r] || e(r);
            s = [function (u) {
                return t[u]
            }
            ];
            e = function () {
                return '\\w+'
            }
            ;
            r = 1
        }
        ;
        while (r--)
            if (s[r])
                p = p.replace(new RegExp('\\b' + e(r) + '\\b', 'g'), s[r]);
        return p
    }(n, 17, 17, o.split('|'), 0, {}));
};
function BaseDecode(c) {
    var d = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
    var e = arguments.length;
    if (e == 3) {
        d = arguments[2]
    }
    ;var f = "";
    var h, i, j;
    var k, l, m, n;
    var o = 0;
    c = c.replace(/[^A-Za-z0-9\+\/\=]/g, "");
    while (o < c.length) {
        k = d.indexOf(c.charAt(o++));
        l = d.indexOf(c.charAt(o++));
        m = d.indexOf(c.charAt(o++));
        n = d.indexOf(c.charAt(o++));
        h = (k << 2) | (l >> 4);
        i = ((l & 15) << 4) | (m >> 2);
        j = ((m & 3) << 6) | n;
        f = f + String.fromCharCode(h);
        if (m != 64) {
            f = f + String.fromCharCode(i)
        }
        ;
        if (n != 64) {
            f = f + String.fromCharCode(j)
        }
    }
    ;
    return f
}

function eee() {
    return GetGuid(20, 16);
}
function sss(n1,o1) {
    return DoTk(n1,o1);
}
