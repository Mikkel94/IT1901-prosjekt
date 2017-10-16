$(function() {
    $('a.level-hint').on('click', function(e) {
        e.preventDefault();
        if ($('.info-hint').length) {
            $('.info-hint').fadeToggle();
        } else {
            $.getJSON('?get-hint', function(data) {
                if (data.status) {
                    $hint = $('<div/>', {
                        html: data.hint,
                        class: 'info info-hint'
                    });
                    $('.level-header').parent().append($hint);
                    var $allVideos = $(".bbcode-youtube, .bbcode-vimeo");
                    $allVideos.each(function() {
                        var $el = $(this);
                        $el.removeAttr('height').height($el.width() * 0.56);
                    });
                    $hint.hide().fadeIn();
                }
            });
        }
    });
});
var timer_start = new Date().getTime();
(function timer() {
    $('.timer').each(function() {
        var now = new Date().getTime();
        var time = now - timer_start;
        time = $(this).attr('data-time') - time / 1000;
        if (time <= 0)
            time = 0;
        $(this).html('Time remaining: <span>' + time.toFixed(2) + ' seconds</span>');
    });
    setTimeout(timer, 100);
})();
var hljs = new function() {
    function l(o) {
        return o.replace(/&/gm, "&amp;").replace(/</gm, "&lt;").replace(/>/gm, "&gt;")
    }

    function b(p) {
        for (var o = p.firstChild; o; o = o.nextSibling) {
            if (o.nodeName == "CODE") {
                return o
            }
            if (!(o.nodeType == 3 && o.nodeValue.match(/\s+/))) {
                break
            }
        }
    }

    function h(p, o) {
        return Array.prototype.map.call(p.childNodes, function(q) {
            if (q.nodeType == 3) {
                return o ? q.nodeValue.replace(/\n/g, "") : q.nodeValue
            }
            if (q.nodeName == "BR") {
                return "\n"
            }
            return h(q, o)
        }).join("")
    }

    function a(q) {
        var p = (q.className + " " + q.parentNode.className).split(/\s+/);
        p = p.map(function(r) {
            return r.replace(/^language-/, "")
        });
        for (var o = 0; o < p.length; o++) {
            if (e[p[o]] || p[o] == "no-highlight") {
                return p[o]
            }
        }
    }

    function c(q) {
        var o = [];
        (function p(r, s) {
            for (var t = r.firstChild; t; t = t.nextSibling) {
                if (t.nodeType == 3) {
                    s += t.nodeValue.length
                } else {
                    if (t.nodeName == "BR") {
                        s += 1
                    } else {
                        if (t.nodeType == 1) {
                            o.push({
                                event: "start",
                                offset: s,
                                node: t
                            });
                            s = p(t, s);
                            o.push({
                                event: "stop",
                                offset: s,
                                node: t
                            })
                        }
                    }
                }
            }
            return s
        })(q, 0);
        return o
    }

    function j(x, v, w) {
        var p = 0;
        var y = "";
        var r = [];

        function t() {
            if (x.length && v.length) {
                if (x[0].offset != v[0].offset) {
                    return (x[0].offset < v[0].offset) ? x : v
                } else {
                    return v[0].event == "start" ? x : v
                }
            } else {
                return x.length ? x : v
            }
        }

        function s(A) {
            function z(B) {
                return " " + B.nodeName + '="' + l(B.value) + '"'
            }
            return "<" + A.nodeName + Array.prototype.map.call(A.attributes, z).join("") + ">"
        }
        while (x.length || v.length) {
            var u = t().splice(0, 1)[0];
            y += l(w.substr(p, u.offset - p));
            p = u.offset;
            if (u.event == "start") {
                y += s(u.node);
                r.push(u.node)
            } else {
                if (u.event == "stop") {
                    var o, q = r.length;
                    do {
                        q--;
                        o = r[q];
                        y += ("</" + o.nodeName.toLowerCase() + ">")
                    } while (o != u.node);
                    r.splice(q, 1);
                    while (q < r.length) {
                        y += s(r[q]);
                        q++
                    }
                }
            }
        }
        return y + l(w.substr(p))
    }

    function f(q) {
        function o(s, r) {
            return RegExp(s, "m" + (q.cI ? "i" : "") + (r ? "g" : ""))
        }

        function p(y, w) {
            if (y.compiled) {
                return
            }
            y.compiled = true;
            var s = [];
            if (y.k) {
                var r = {};

                function z(A, t) {
                    t.split(" ").forEach(function(B) {
                        var C = B.split("|");
                        r[C[0]] = [A, C[1] ? Number(C[1]) : 1];
                        s.push(C[0])
                    })
                }
                y.lR = o(y.l || hljs.IR, true);
                if (typeof y.k == "string") {
                    z("keyword", y.k)
                } else {
                    for (var x in y.k) {
                        if (!y.k.hasOwnProperty(x)) {
                            continue
                        }
                        z(x, y.k[x])
                    }
                }
                y.k = r
            }
            if (w) {
                if (y.bWK) {
                    y.b = "\\b(" + s.join("|") + ")\\s"
                }
                y.bR = o(y.b ? y.b : "\\B|\\b");
                if (!y.e && !y.eW) {
                    y.e = "\\B|\\b"
                }
                if (y.e) {
                    y.eR = o(y.e)
                }
                y.tE = y.e || "";
                if (y.eW && w.tE) {
                    y.tE += (y.e ? "|" : "") + w.tE
                }
            }
            if (y.i) {
                y.iR = o(y.i)
            }
            if (y.r === undefined) {
                y.r = 1
            }
            if (!y.c) {
                y.c = []
            }
            for (var v = 0; v < y.c.length; v++) {
                if (y.c[v] == "self") {
                    y.c[v] = y
                }
                p(y.c[v], y)
            }
            if (y.starts) {
                p(y.starts, w)
            }
            var u = [];
            for (var v = 0; v < y.c.length; v++) {
                u.push(y.c[v].b)
            }
            if (y.tE) {
                u.push(y.tE)
            }
            if (y.i) {
                u.push(y.i)
            }
            y.t = u.length ? o(u.join("|"), true) : {
                exec: function(t) {
                    return null
                }
            }
        }
        p(q)
    }

    function d(D, E) {
        function o(r, M) {
            for (var L = 0; L < M.c.length; L++) {
                var K = M.c[L].bR.exec(r);
                if (K && K.index == 0) {
                    return M.c[L]
                }
            }
        }

        function s(K, r) {
            if (K.e && K.eR.test(r)) {
                return K
            }
            if (K.eW) {
                return s(K.parent, r)
            }
        }

        function t(r, K) {
            return K.i && K.iR.test(r)
        }

        function y(L, r) {
            var K = F.cI ? r[0].toLowerCase() : r[0];
            return L.k.hasOwnProperty(K) && L.k[K]
        }

        function G() {
            var K = l(w);
            if (!A.k) {
                return K
            }
            var r = "";
            var N = 0;
            A.lR.lastIndex = 0;
            var L = A.lR.exec(K);
            while (L) {
                r += K.substr(N, L.index - N);
                var M = y(A, L);
                if (M) {
                    v += M[1];
                    r += '<span class="' + M[0] + '">' + L[0] + "</span>"
                } else {
                    r += L[0]
                }
                N = A.lR.lastIndex;
                L = A.lR.exec(K)
            }
            return r + K.substr(N)
        }

        function z() {
            if (A.sL && !e[A.sL]) {
                return l(w)
            }
            var r = A.sL ? d(A.sL, w) : g(w);
            if (A.r > 0) {
                v += r.keyword_count;
                B += r.r
            }
            return '<span class="' + r.language + '">' + r.value + "</span>"
        }

        function J() {
            return A.sL !== undefined ? z() : G()
        }

        function I(L, r) {
            var K = L.cN ? '<span class="' + L.cN + '">' : "";
            if (L.rB) {
                x += K;
                w = ""
            } else {
                if (L.eB) {
                    x += l(r) + K;
                    w = ""
                } else {
                    x += K;
                    w = r
                }
            }
            A = Object.create(L, {
                parent: {
                    value: A
                }
            });
            B += L.r
        }

        function C(K, r) {
            w += K;
            if (r === undefined) {
                x += J();
                return 0
            }
            var L = o(r, A);
            if (L) {
                x += J();
                I(L, r);
                return L.rB ? 0 : r.length
            }
            var M = s(A, r);
            if (M) {
                if (!(M.rE || M.eE)) {
                    w += r
                }
                x += J();
                do {
                    if (A.cN) {
                        x += "</span>"
                    }
                    A = A.parent
                } while (A != M.parent);
                if (M.eE) {
                    x += l(r)
                }
                w = "";
                if (M.starts) {
                    I(M.starts, "")
                }
                return M.rE ? 0 : r.length
            }
            if (t(r, A)) {
                throw "Illegal"
            }
            w += r;
            return r.length || 1
        }
        var F = e[D];
        f(F);
        var A = F;
        var w = "";
        var B = 0;
        var v = 0;
        var x = "";
        try {
            var u, q, p = 0;
            while (true) {
                A.t.lastIndex = p;
                u = A.t.exec(E);
                if (!u) {
                    break
                }
                q = C(E.substr(p, u.index - p), u[0]);
                p = u.index + q
            }
            C(E.substr(p));
            return {
                r: B,
                keyword_count: v,
                value: x,
                language: D
            }
        } catch (H) {
            if (H == "Illegal") {
                return {
                    r: 0,
                    keyword_count: 0,
                    value: l(E)
                }
            } else {
                throw H
            }
        }
    }

    function g(s) {
        var o = {
            keyword_count: 0,
            r: 0,
            value: l(s)
        };
        var q = o;
        for (var p in e) {
            if (!e.hasOwnProperty(p)) {
                continue
            }
            var r = d(p, s);
            r.language = p;
            if (r.keyword_count + r.r > q.keyword_count + q.r) {
                q = r
            }
            if (r.keyword_count + r.r > o.keyword_count + o.r) {
                q = o;
                o = r
            }
        }
        if (q.language) {
            o.second_best = q
        }
        return o
    }

    function i(q, p, o) {
        if (p) {
            q = q.replace(/^((<[^>]+>|\t)+)/gm, function(r, v, u, t) {
                return v.replace(/\t/g, p)
            })
        }
        if (o) {
            q = q.replace(/\n/g, "<br>")
        }
        return q
    }

    function m(r, u, p) {
        var v = h(r, p);
        var t = a(r);
        if (t == "no-highlight") {
            return
        }
        var w = t ? d(t, v) : g(v);
        t = w.language;
        var o = c(r);
        if (o.length) {
            var q = document.createElement("pre");
            q.innerHTML = w.value;
            w.value = j(o, c(q), v)
        }
        w.value = i(w.value, u, p);
        var s = r.className;
        if (!s.match("(\\s|^)(language-)?" + t + "(\\s|$)")) {
            s = s ? (s + " " + t) : t
        }
        r.innerHTML = w.value;
        r.className = s;
        r.result = {
            language: t,
            kw: w.keyword_count,
            re: w.r
        };
        if (w.second_best) {
            r.second_best = {
                language: w.second_best.language,
                kw: w.second_best.keyword_count,
                re: w.second_best.r
            }
        }
    }

    function n() {
        if (n.called) {
            return
        }
        n.called = true;
        Array.prototype.map.call(document.getElementsByTagName("pre"), b).filter(Boolean).forEach(function(o) {
            m(o, hljs.tabReplace)
        })
    }

    function k() {
        window.addEventListener("DOMContentLoaded", n, false);
        window.addEventListener("load", n, false)
    }
    var e = {};
    this.LANGUAGES = e;
    this.highlight = d;
    this.highlightAuto = g;
    this.fixMarkup = i;
    this.highlightBlock = m;
    this.initHighlighting = n;
    this.initHighlightingOnLoad = k;
    this.IR = "[a-zA-Z][a-zA-Z0-9_]*";
    this.UIR = "[a-zA-Z_][a-zA-Z0-9_]*";
    this.NR = "\\b\\d+(\\.\\d+)?";
    this.CNR = "(\\b0[xX][a-fA-F0-9]+|(\\b\\d+(\\.\\d*)?|\\.\\d+)([eE][-+]?\\d+)?)";
    this.BNR = "\\b(0b[01]+)";
    this.RSR = "!|!=|!==|%|%=|&|&&|&=|\\*|\\*=|\\+|\\+=|,|\\.|-|-=|/|/=|:|;|<|<<|<<=|<=|=|==|===|>|>=|>>|>>=|>>>|>>>=|\\?|\\[|\\{|\\(|\\^|\\^=|\\||\\|=|\\|\\||~";
    this.BE = {
        b: "\\\\[\\s\\S]",
        r: 0
    };
    this.ASM = {
        cN: "string",
        b: "'",
        e: "'",
        i: "\\n",
        c: [this.BE],
        r: 0
    };
    this.QSM = {
        cN: "string",
        b: '"',
        e: '"',
        i: "\\n",
        c: [this.BE],
        r: 0
    };
    this.CLCM = {
        cN: "comment",
        b: "//",
        e: "$"
    };
    this.CBLCLM = {
        cN: "comment",
        b: "/\\*",
        e: "\\*/"
    };
    this.HCM = {
        cN: "comment",
        b: "#",
        e: "$"
    };
    this.NM = {
        cN: "number",
        b: this.NR,
        r: 0
    };
    this.CNM = {
        cN: "number",
        b: this.CNR,
        r: 0
    };
    this.BNM = {
        cN: "number",
        b: this.BNR,
        r: 0
    };
    this.inherit = function(q, r) {
        var o = {};
        for (var p in q) {
            o[p] = q[p]
        }
        if (r) {
            for (var p in r) {
                o[p] = r[p]
            }
        }
        return o
    }
}();
hljs.LANGUAGES.bash = function(a) {
    var g = "true false";
    var e = "if then else elif fi for break continue while in do done echo exit return set declare";
    var c = {
        cN: "variable",
        b: "\\$[a-zA-Z0-9_#]+"
    };
    var b = {
        cN: "variable",
        b: "\\${([^}]|\\\\})+}"
    };
    var h = {
        cN: "string",
        b: '"',
        e: '"',
        i: "\\n",
        c: [a.BE, c, b],
        r: 0
    };
    var d = {
        cN: "string",
        b: "'",
        e: "'",
        c: [{
            b: "''"
        }],
        r: 0
    };
    var f = {
        cN: "test_condition",
        b: "",
        e: "",
        c: [h, d, c, b],
        k: {
            literal: g
        },
        r: 0
    };
    return {
        k: {
            keyword: e,
            literal: g
        },
        c: [{
            cN: "shebang",
            b: "(#!\\/bin\\/bash)|(#!\\/bin\\/sh)",
            r: 10
        }, c, b, a.HCM, h, d, a.inherit(f, {
            b: "\\[ ",
            e: " \\]",
            r: 0
        }), a.inherit(f, {
            b: "\\[\\[ ",
            e: " \\]\\]"
        })]
    }
}(hljs);
hljs.LANGUAGES.cs = function(a) {
    return {
        k: "abstract as base bool break byte case catch char checked class const continue decimal default delegate do double else enum event explicit extern false finally fixed float for foreach goto if implicit in int interface internal is lock long namespace new null object operator out override params private protected public readonly ref return sbyte sealed short sizeof stackalloc static string struct switch this throw true try typeof uint ulong unchecked unsafe ushort using virtual volatile void while ascending descending from get group into join let orderby partial select set value var where yield",
        c: [{
            cN: "comment",
            b: "///",
            e: "$",
            rB: true,
            c: [{
                cN: "xmlDocTag",
                b: "///|<!--|-->"
            }, {
                cN: "xmlDocTag",
                b: "</?",
                e: ">"
            }]
        }, a.CLCM, a.CBLCLM, {
            cN: "preprocessor",
            b: "#",
            e: "$",
            k: "if else elif endif define undef warning error line region endregion pragma checksum"
        }, {
            cN: "string",
            b: '@"',
            e: '"',
            c: [{
                b: '""'
            }]
        }, a.ASM, a.QSM, a.CNM]
    }
}(hljs);
hljs.LANGUAGES.ruby = function(e) {
    var a = "[a-zA-Z_][a-zA-Z0-9_]*(\\!|\\?)?";
    var j = "[a-zA-Z_]\\w*[!?=]?|[-+~]\\@|<<|>>|=~|===?|<=>|[<>]=?|\\*\\*|[-/+%^&*~`|]|\\[\\]=?";
    var g = {
        keyword: "and false then defined module in return redo if BEGIN retry end for true self when next until do begin unless END rescue nil else break undef not super class case require yield alias while ensure elsif or include"
    };
    var c = {
        cN: "yardoctag",
        b: "@[A-Za-z]+"
    };
    var k = [{
        cN: "comment",
        b: "#",
        e: "$",
        c: [c]
    }, {
        cN: "comment",
        b: "^\\=begin",
        e: "^\\=end",
        c: [c],
        r: 10
    }, {
        cN: "comment",
        b: "^__END__",
        e: "\\n$"
    }];
    var d = {
        cN: "subst",
        b: "#\\{",
        e: "}",
        l: a,
        k: g
    };
    var i = [e.BE, d];
    var b = [{
        cN: "string",
        b: "'",
        e: "'",
        c: i,
        r: 0
    }, {
        cN: "string",
        b: '"',
        e: '"',
        c: i,
        r: 0
    }, {
        cN: "string",
        b: "%[qw]?\\(",
        e: "\\)",
        c: i
    }, {
        cN: "string",
        b: "%[qw]?\\[",
        e: "\\]",
        c: i
    }, {
        cN: "string",
        b: "%[qw]?{",
        e: "}",
        c: i
    }, {
        cN: "string",
        b: "%[qw]?<",
        e: ">",
        c: i,
        r: 10
    }, {
        cN: "string",
        b: "%[qw]?/",
        e: "/",
        c: i,
        r: 10
    }, {
        cN: "string",
        b: "%[qw]?%",
        e: "%",
        c: i,
        r: 10
    }, {
        cN: "string",
        b: "%[qw]?-",
        e: "-",
        c: i,
        r: 10
    }, {
        cN: "string",
        b: "%[qw]?\\|",
        e: "\\|",
        c: i,
        r: 10
    }];
    var h = {
        cN: "function",
        bWK: true,
        e: " |$|;",
        k: "def",
        c: [{
            cN: "title",
            b: j,
            l: a,
            k: g
        }, {
            cN: "params",
            b: "\\(",
            e: "\\)",
            l: a,
            k: g
        }].concat(k)
    };
    var f = k.concat(b.concat([{
        cN: "class",
        bWK: true,
        e: "$|;",
        k: "class module",
        c: [{
            cN: "title",
            b: "[A-Za-z_]\\w*(::\\w+)*(\\?|\\!)?",
            r: 0
        }, {
            cN: "inheritance",
            b: "<\\s*",
            c: [{
                cN: "parent",
                b: "(" + e.IR + "::)?" + e.IR
            }]
        }].concat(k)
    }, h, {
        cN: "constant",
        b: "(::)?(\\b[A-Z]\\w*(::)?)+",
        r: 0
    }, {
        cN: "symbol",
        b: ":",
        c: b.concat([{
            b: j
        }]),
        r: 0
    }, {
        cN: "symbol",
        b: a + ":",
        r: 0
    }, {
        cN: "number",
        b: "(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b",
        r: 0
    }, {
        cN: "number",
        b: "\\?\\w"
    }, {
        cN: "variable",
        b: "(\\$\\W)|((\\$|\\@\\@?)(\\w+))"
    }, {
        b: "(" + e.RSR + ")\\s*",
        c: k.concat([{
            cN: "regexp",
            b: "/",
            e: "/[a-z]*",
            i: "\\n",
            c: [e.BE, d]
        }]),
        r: 0
    }]));
    d.c = f;
    h.c[1].c = f;
    return {
        l: a,
        k: g,
        c: f
    }
}(hljs);
hljs.LANGUAGES.javascript = function(a) {
    return {
        k: {
            keyword: "in if for while finally var new function do return void else break catch instanceof with throw case default try this switch continue typeof delete let yield const",
            literal: "true false null undefined NaN Infinity"
        },
        c: [a.ASM, a.QSM, a.CLCM, a.CBLCLM, a.CNM, {
            b: "(" + a.RSR + "|\\b(case|return|throw)\\b)\\s*",
            k: "return throw case",
            c: [a.CLCM, a.CBLCLM, {
                cN: "regexp",
                b: "/",
                e: "/[gim]*",
                i: "\\n",
                c: [{
                    b: "\\\\/"
                }]
            }, {
                b: "<",
                e: ">;",
                sL: "xml"
            }],
            r: 0
        }, {
            cN: "function",
            bWK: true,
            e: "{",
            k: "function",
            c: [{
                cN: "title",
                b: "[A-Za-z$_][0-9A-Za-z$_]*"
            }, {
                cN: "params",
                b: "\\(",
                e: "\\)",
                c: [a.CLCM, a.CBLCLM],
                i: "[\"'\\(]"
            }],
            i: "\\[|%"
        }]
    }
}(hljs);
hljs.LANGUAGES.css = function(a) {
    var b = {
        cN: "function",
        b: a.IR + "\\(",
        e: "\\)",
        c: [a.NM, a.ASM, a.QSM]
    };
    return {
        cI: true,
        i: "[=/|']",
        c: [a.CBLCLM, {
            cN: "id",
            b: "\\#[A-Za-z0-9_-]+"
        }, {
            cN: "class",
            b: "\\.[A-Za-z0-9_-]+",
            r: 0
        }, {
            cN: "attr_selector",
            b: "\\[",
            e: "\\]",
            i: "$"
        }, {
            cN: "pseudo",
            b: ":(:)?[a-zA-Z0-9\\_\\-\\+\\(\\)\\\"\\']+"
        }, {
            cN: "at_rule",
            b: "@(font-face|page)",
            l: "[a-z-]+",
            k: "font-face page"
        }, {
            cN: "at_rule",
            b: "@",
            e: "[{;]",
            eE: true,
            k: "import page media charset",
            c: [b, a.ASM, a.QSM, a.NM]
        }, {
            cN: "tag",
            b: a.IR,
            r: 0
        }, {
            cN: "rules",
            b: "{",
            e: "}",
            i: "[^\\s]",
            r: 0,
            c: [a.CBLCLM, {
                cN: "rule",
                b: "[^\\s]",
                rB: true,
                e: ";",
                eW: true,
                c: [{
                    cN: "attribute",
                    b: "[A-Z\\_\\.\\-]+",
                    e: ":",
                    eE: true,
                    i: "[^\\s]",
                    starts: {
                        cN: "value",
                        eW: true,
                        eE: true,
                        c: [b, a.NM, a.QSM, a.ASM, a.CBLCLM, {
                            cN: "hexcolor",
                            b: "\\#[0-9A-F]+"
                        }, {
                            cN: "important",
                            b: "!important"
                        }]
                    }
                }]
            }]
        }]
    }
}(hljs);
hljs.LANGUAGES.xml = function(a) {
    var c = "[A-Za-z0-9\\._:-]+";
    var b = {
        eW: true,
        c: [{
            cN: "attribute",
            b: c,
            r: 0
        }, {
            b: '="',
            rB: true,
            e: '"',
            c: [{
                cN: "value",
                b: '"',
                eW: true
            }]
        }, {
            b: "='",
            rB: true,
            e: "'",
            c: [{
                cN: "value",
                b: "'",
                eW: true
            }]
        }, {
            b: "=",
            c: [{
                cN: "value",
                b: "[^\\s/>]+"
            }]
        }]
    };
    return {
        cI: true,
        c: [{
            cN: "pi",
            b: "<\\?",
            e: "\\?>",
            r: 10
        }, {
            cN: "doctype",
            b: "<!DOCTYPE",
            e: ">",
            r: 10,
            c: [{
                b: "\\[",
                e: "\\]"
            }]
        }, {
            cN: "comment",
            b: "<!--",
            e: "-->",
            r: 10
        }, {
            cN: "cdata",
            b: "<\\!\\[CDATA\\[",
            e: "\\]\\]>",
            r: 10
        }, {
            cN: "tag",
            b: "<style(?=\\s|>|$)",
            e: ">",
            k: {
                title: "style"
            },
            c: [b],
            starts: {
                e: "</style>",
                rE: true,
                sL: "css"
            }
        }, {
            cN: "tag",
            b: "<script(?=\\s|>|$)",
            e: ">",
            k: {
                title: "script"
            },
            c: [b],
            starts: {
                e: "<\/script>",
                rE: true,
                sL: "javascript"
            }
        }, {
            b: "<%",
            e: "%>",
            sL: "vbscript"
        }, {
            cN: "tag",
            b: "</?",
            e: "/?>",
            c: [{
                cN: "title",
                b: "[^ />]+"
            }, b]
        }]
    }
}(hljs);
hljs.LANGUAGES.http = function(a) {
    return {
        i: "\\S",
        c: [{
            cN: "status",
            b: "^HTTP/[0-9\\.]+",
            e: "$",
            c: [{
                cN: "number",
                b: "\\b\\d{3}\\b"
            }]
        }, {
            cN: "request",
            b: "^[A-Z]+ (.*?) HTTP/[0-9\\.]+$",
            rB: true,
            e: "$",
            c: [{
                cN: "string",
                b: " ",
                e: " ",
                eB: true,
                eE: true
            }]
        }, {
            cN: "attribute",
            b: "^\\w",
            e: ": ",
            eE: true,
            i: "\\n|\\s|=",
            starts: {
                cN: "string",
                e: "$"
            }
        }, {
            b: "\\n\\n",
            starts: {
                sL: "",
                eW: true
            }
        }]
    }
}(hljs);
hljs.LANGUAGES.java = function(a) {
    return {
        k: "false synchronized int abstract float private char boolean static null if const for true while long throw strictfp finally protected import native final return void enum else break transient new catch instanceof byte super volatile case assert short package default double public try this switch continue throws",
        c: [{
            cN: "javadoc",
            b: "/\\*\\*",
            e: "\\*/",
            c: [{
                cN: "javadoctag",
                b: "@[A-Za-z]+"
            }],
            r: 10
        }, a.CLCM, a.CBLCLM, a.ASM, a.QSM, {
            cN: "class",
            bWK: true,
            e: "{",
            k: "class interface",
            i: ":",
            c: [{
                bWK: true,
                k: "extends implements",
                r: 10
            }, {
                cN: "title",
                b: a.UIR
            }]
        }, a.CNM, {
            cN: "annotation",
            b: "@[A-Za-z]+"
        }]
    }
}(hljs);
hljs.LANGUAGES.php = function(a) {
    var e = {
        cN: "variable",
        b: "\\$+[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*"
    };
    var b = [a.inherit(a.ASM, {
        i: null
    }), a.inherit(a.QSM, {
        i: null
    }), {
        cN: "string",
        b: 'b"',
        e: '"',
        c: [a.BE]
    }, {
        cN: "string",
        b: "b'",
        e: "'",
        c: [a.BE]
    }];
    var c = [a.BNM, a.CNM];
    var d = {
        cN: "title",
        b: a.UIR
    };
    return {
        cI: true,
        k: "and include_once list abstract global private echo interface as static endswitch array null if endwhile or const for endforeach self var while isset public protected exit foreach throw elseif include __FILE__ empty require_once do xor return implements parent clone use __CLASS__ __LINE__ else break print eval new catch __METHOD__ case exception php_user_filter default die require __FUNCTION__ enddeclare final try this switch continue endfor endif declare unset true false namespace trait goto instanceof insteadof __DIR__ __NAMESPACE__ __halt_compiler",
        c: [a.CLCM, a.HCM, {
            cN: "comment",
            b: "/\\*",
            e: "\\*/",
            c: [{
                cN: "phpdoc",
                b: "\\s@[A-Za-z]+"
            }]
        }, {
            cN: "comment",
            eB: true,
            b: "__halt_compiler.+?;",
            eW: true
        }, {
            cN: "string",
            b: "<<<['\"]?\\w+['\"]?$",
            e: "^\\w+;",
            c: [a.BE]
        }, {
            cN: "preprocessor",
            b: "<\\?php",
            r: 10
        }, {
            cN: "preprocessor",
            b: "\\?>"
        }, e, {
            cN: "function",
            bWK: true,
            e: "{",
            k: "function",
            i: "\\$|\\[|%",
            c: [d, {
                cN: "params",
                b: "\\(",
                e: "\\)",
                c: ["self", e, a.CBLCLM].concat(b).concat(c)
            }]
        }, {
            cN: "class",
            bWK: true,
            e: "{",
            k: "class",
            i: "[:\\(\\$]",
            c: [{
                bWK: true,
                eW: true,
                k: "extends",
                c: [d]
            }, d]
        }, {
            b: "=>"
        }].concat(b).concat(c)
    }
}(hljs);
hljs.LANGUAGES.python = function(a) {
    var f = {
        cN: "prompt",
        b: "^(>>>|\\.\\.\\.) "
    };
    var c = [{
        cN: "string",
        b: "(u|b)?r?'''",
        e: "'''",
        c: [f],
        r: 10
    }, {
        cN: "string",
        b: '(u|b)?r?"""',
        e: '"""',
        c: [f],
        r: 10
    }, {
        cN: "string",
        b: "(u|r|ur)'",
        e: "'",
        c: [a.BE],
        r: 10
    }, {
        cN: "string",
        b: '(u|r|ur)"',
        e: '"',
        c: [a.BE],
        r: 10
    }, {
        cN: "string",
        b: "(b|br)'",
        e: "'",
        c: [a.BE]
    }, {
        cN: "string",
        b: '(b|br)"',
        e: '"',
        c: [a.BE]
    }].concat([a.ASM, a.QSM]);
    var e = {
        cN: "title",
        b: a.UIR
    };
    var d = {
        cN: "params",
        b: "\\(",
        e: "\\)",
        c: ["self", a.CNM, f].concat(c)
    };
    var b = {
        bWK: true,
        e: ":",
        i: "[${=;\\n]",
        c: [e, d],
        r: 10
    };
    return {
        k: {
            keyword: "and elif is global as in if from raise for except finally print import pass return exec else break not with class assert yield try while continue del or def lambda nonlocal|10",
            built_in: "None True False Ellipsis NotImplemented"
        },
        i: "(</|->|\\?)",
        c: c.concat([f, a.HCM, a.inherit(b, {
            cN: "function",
            k: "def"
        }), a.inherit(b, {
            cN: "class",
            k: "class"
        }), a.CNM, {
            cN: "decorator",
            b: "@",
            e: "$"
        }, {
            b: "\\b(print|exec)\\("
        }])
    }
}(hljs);
hljs.LANGUAGES.sql = function(a) {
    return {
        cI: true,
        c: [{
            cN: "operator",
            b: "(begin|start|commit|rollback|savepoint|lock|alter|create|drop|rename|call|delete|do|handler|insert|load|replace|select|truncate|update|set|show|pragma|grant)\\b(?!:)",
            e: ";",
            eW: true,
            k: {
                keyword: "all partial global month current_timestamp using go revoke smallint indicator end-exec disconnect zone with character assertion to add current_user usage input local alter match collate real then rollback get read timestamp session_user not integer bit unique day minute desc insert execute like ilike|2 level decimal drop continue isolation found where constraints domain right national some module transaction relative second connect escape close system_user for deferred section cast current sqlstate allocate intersect deallocate numeric public preserve full goto initially asc no key output collation group by union session both last language constraint column of space foreign deferrable prior connection unknown action commit view or first into float year primary cascaded except restrict set references names table outer open select size are rows from prepare distinct leading create only next inner authorization schema corresponding option declare precision immediate else timezone_minute external varying translation true case exception join hour default double scroll value cursor descriptor values dec fetch procedure delete and false int is describe char as at in varchar null trailing any absolute current_time end grant privileges when cross check write current_date pad begin temporary exec time update catalog user sql date on identity timezone_hour natural whenever interval work order cascade diagnostics nchar having left call do handler load replace truncate start lock show pragma exists number",
                aggregate: "count sum min max avg"
            },
            c: [{
                cN: "string",
                b: "'",
                e: "'",
                c: [a.BE, {
                    b: "''"
                }],
                r: 0
            }, {
                cN: "string",
                b: '"',
                e: '"',
                c: [a.BE, {
                    b: '""'
                }],
                r: 0
            }, {
                cN: "string",
                b: "`",
                e: "`",
                c: [a.BE]
            }, a.CNM]
        }, a.CBLCLM, {
            cN: "comment",
            b: "--",
            e: "$"
        }]
    }
}(hljs);
hljs.LANGUAGES.ini = function(a) {
    return {
        cI: true,
        i: "[^\\s]",
        c: [{
            cN: "comment",
            b: ";",
            e: "$"
        }, {
            cN: "title",
            b: "^\\[",
            e: "\\]"
        }, {
            cN: "setting",
            b: "^[a-z0-9\\[\\]_-]+[ \\t]*=[ \\t]*",
            e: "$",
            c: [{
                cN: "value",
                eW: true,
                k: "on off true false yes no",
                c: [a.QSM, a.NM]
            }]
        }]
    }
}(hljs);
hljs.LANGUAGES.perl = function(e) {
    var a = "getpwent getservent quotemeta msgrcv scalar kill dbmclose undef lc ma syswrite tr send umask sysopen shmwrite vec qx utime local oct semctl localtime readpipe do return format read sprintf dbmopen pop getpgrp not getpwnam rewinddir qqfileno qw endprotoent wait sethostent bless s|0 opendir continue each sleep endgrent shutdown dump chomp connect getsockname die socketpair close flock exists index shmgetsub for endpwent redo lstat msgctl setpgrp abs exit select print ref gethostbyaddr unshift fcntl syscall goto getnetbyaddr join gmtime symlink semget splice x|0 getpeername recv log setsockopt cos last reverse gethostbyname getgrnam study formline endhostent times chop length gethostent getnetent pack getprotoent getservbyname rand mkdir pos chmod y|0 substr endnetent printf next open msgsnd readdir use unlink getsockopt getpriority rindex wantarray hex system getservbyport endservent int chr untie rmdir prototype tell listen fork shmread ucfirst setprotoent else sysseek link getgrgid shmctl waitpid unpack getnetbyname reset chdir grep split require caller lcfirst until warn while values shift telldir getpwuid my getprotobynumber delete and sort uc defined srand accept package seekdir getprotobyname semop our rename seek if q|0 chroot sysread setpwent no crypt getc chown sqrt write setnetent setpriority foreach tie sin msgget map stat getlogin unless elsif truncate exec keys glob tied closedirioctl socket readlink eval xor readline binmode setservent eof ord bind alarm pipe atan2 getgrent exp time push setgrent gt lt or ne m|0 break given say state when";
    var d = {
        cN: "subst",
        b: "[$@]\\{",
        e: "\\}",
        k: a,
        r: 10
    };
    var b = {
        cN: "variable",
        b: "\\$\\d"
    };
    var i = {
        cN: "variable",
        b: "[\\$\\%\\@\\*](\\^\\w\\b|#\\w+(\\:\\:\\w+)*|[^\\s\\w{]|{\\w+}|\\w+(\\:\\:\\w*)*)"
    };
    var f = [e.BE, d, b, i];
    var h = {
        b: "->",
        c: [{
            b: e.IR
        }, {
            b: "{",
            e: "}"
        }]
    };
    var g = {
        cN: "comment",
        b: "^(__END__|__DATA__)",
        e: "\\n$",
        r: 5
    };
    var c = [b, i, e.HCM, g, {
        cN: "comment",
        b: "^\\=\\w",
        e: "\\=cut",
        eW: true
    }, h, {
        cN: "string",
        b: "q[qwxr]?\\s*\\(",
        e: "\\)",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "q[qwxr]?\\s*\\[",
        e: "\\]",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "q[qwxr]?\\s*\\{",
        e: "\\}",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "q[qwxr]?\\s*\\|",
        e: "\\|",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "q[qwxr]?\\s*\\<",
        e: "\\>",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "qw\\s+q",
        e: "q",
        c: f,
        r: 5
    }, {
        cN: "string",
        b: "'",
        e: "'",
        c: [e.BE],
        r: 0
    }, {
        cN: "string",
        b: '"',
        e: '"',
        c: f,
        r: 0
    }, {
        cN: "string",
        b: "`",
        e: "`",
        c: [e.BE]
    }, {
        cN: "string",
        b: "{\\w+}",
        r: 0
    }, {
        cN: "string",
        b: "-?\\w+\\s*\\=\\>",
        r: 0
    }, {
        cN: "number",
        b: "(\\b0[0-7_]+)|(\\b0x[0-9a-fA-F_]+)|(\\b[1-9][0-9_]*(\\.[0-9_]+)?)|[0_]\\b",
        r: 0
    }, {
        b: "(" + e.RSR + "|\\b(split|return|print|reverse|grep)\\b)\\s*",
        k: "split return print reverse grep",
        r: 0,
        c: [e.HCM, g, {
            cN: "regexp",
            b: "(s|tr|y)/(\\\\.|[^/])*/(\\\\.|[^/])*/[a-z]*",
            r: 10
        }, {
            cN: "regexp",
            b: "(m|qr)?/",
            e: "/[a-z]*",
            c: [e.BE],
            r: 0
        }]
    }, {
        cN: "sub",
        bWK: true,
        e: "(\\s*\\(.*?\\))?[;{]",
        k: "sub",
        r: 5
    }, {
        cN: "operator",
        b: "-\\w\\b",
        r: 0
    }];
    d.c = c;
    h.c[1].c = c;
    return {
        k: a,
        c: c
    }
}(hljs);
hljs.LANGUAGES.json = function(a) {
    var e = {
        literal: "true false null"
    };
    var d = [a.QSM, a.CNM];
    var c = {
        cN: "value",
        e: ",",
        eW: true,
        eE: true,
        c: d,
        k: e
    };
    var b = {
        b: "{",
        e: "}",
        c: [{
            cN: "attribute",
            b: '\\s*"',
            e: '"\\s*:\\s*',
            eB: true,
            eE: true,
            c: [a.BE],
            i: "\\n",
            starts: c
        }],
        i: "\\S"
    };
    var f = {
        b: "\\[",
        e: "\\]",
        c: [a.inherit(c, {
            cN: null
        })],
        i: "\\S"
    };
    d.splice(d.length, 0, b, f);
    return {
        c: d,
        k: e,
        i: "\\S"
    }
}(hljs);
hljs.LANGUAGES.cpp = function(a) {
    var b = {
        keyword: "false int float while private char catch export virtual operator sizeof dynamic_cast|10 typedef const_cast|10 const struct for static_cast|10 union namespace unsigned long throw volatile static protected bool template mutable if public friend do return goto auto void enum else break new extern using true class asm case typeid short reinterpret_cast|10 default double register explicit signed typename try this switch continue wchar_t inline delete alignof char16_t char32_t constexpr decltype noexcept nullptr static_assert thread_local restrict _Bool complex",
        built_in: "std string cin cout cerr clog stringstream istringstream ostringstream auto_ptr deque list queue stack vector map set bitset multiset multimap unordered_set unordered_map unordered_multiset unordered_multimap array shared_ptr"
    };
    return {
        k: b,
        i: "</",
        c: [a.CLCM, a.CBLCLM, a.QSM, {
            cN: "string",
            b: "'\\\\?.",
            e: "'",
            i: "."
        }, {
            cN: "number",
            b: "\\b(\\d+(\\.\\d*)?|\\.\\d+)(u|U|l|L|ul|UL|f|F)"
        }, a.CNM, {
            cN: "preprocessor",
            b: "#",
            e: "$"
        }, {
            cN: "stl_container",
            b: "\\b(deque|list|queue|stack|vector|map|set|bitset|multiset|multimap|unordered_map|unordered_set|unordered_multiset|unordered_multimap|array)\\s*<",
            e: ">",
            k: b,
            r: 10,
            c: ["self"]
        }]
    }
}(hljs);
$(function() {
    $('pre.bbcode_code_body').each(function(i, e) {
        hljs.highlightBlock(e)
    });
    $('body').on('click', '.bbcode_spoiler_head', function(e) {
        e.preventDefault();
        $(this).toggleClass('active');
    });
    var $allVideos = $(".bbcode-youtube, .bbcode-vimeo");

    function resizeVideos() {
        $allVideos.each(function() {
            var $el = $(this);
            $el.removeAttr('height').height($el.width() * 0.56);
        });
    }
    $(window).resize(resizeVideos).resize();
});
(function(jQuery) {
    var dataKey = jQuery('body').attr('data-key');
    if (typeof dataKey !== 'string' || dataKey === '') return;
    var TOKEN_NAME = 'ajax_csrf_token';
    var TOKEN_VALUE = dataKey;
    var ALLOWED_HOSTNAMES = ['www.hackthis.co.uk', 'hackthis.co.uk', 'localhost'];
    var TOKEN_STRING = TOKEN_NAME + '=' + TOKEN_VALUE;
    jQuery.ajaxPrefilter(function(options) {
        var tempLink = document.createElement("a");
        tempLink.href = options.url;
        var hostname = tempLink.hostname || window.location.hostname;
        if (ALLOWED_HOSTNAMES.indexOf(hostname) > -1) {
            var urlParts = options.url.split('?');
            var queryString = urlParts[1];
            if (typeof queryString === 'undefined') {
                queryString = TOKEN_STRING;
            } else if (queryString.indexOf(TOKEN_NAME) === -1) {
                queryString = TOKEN_STRING + '&' + queryString;
            }
            options.url = urlParts[0] + '?' + queryString;
        }
    });
})(jQuery);
var socket = null;
if (typeof io !== 'undefined') {
    socket = io.connect('https://www.hackthis.co.uk:8080/', {
        secure: true
    });
}
var favcounter = new FavCounter();
var counter_chat = 0;
var counter_notifications = 0;
$(function() {
    var username = $('body').attr('data-username');
    var key = $('body').attr('data-key');
    var feedTmpl = '<tmpl>' + '    <li>' + '      <div class="col span_18">' + '        {{if type == "join"}}' + '            <i class="icon-user"></i><a href="/user/${username}">${username}</a>' + '        {{else type == "friend"}}' + '            <i class="icon-addfriend"></i><a href="/user/${username}">${username}</a> <span class="dark">and</span> <a href="/user/${username_2}">${username_2}</a>' + '        {{else type == "medal"}}' + '            <i class="icon-trophy colour-${uri}"></i><a href="/medals.php#${title.toLowerCase()}">${title}</a> <span class="dark">to</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "comment"}}' + '            <i class="icon-comments"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "forum_post"}}' + '            <i class="icon-chat"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "favourite"}}' + '            <i class="icon-heart"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "article"}}' + '            <i class="icon-books"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "news"}}' + '            <i class="icon-article"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{else type == "level"}}' + '            <i class="icon-good"></i><a href="${uri}">${title}</a> <span class="dark">by</span> <a href="/user/${username}">${username}</a>' + '        {{/if}}' + '        </div>' + '        <div class="col span_6 time right"><time class="short" datetime="${timestamp}"></time></div>' + '    </li>' + '</tmpl>';
    if (socket) {
        socket.on('feed', function(data) {
            var item = $(feedTmpl).tmpl(data);
            if ($('.sidebar .feed ul').length) {
                item.hide().prependTo($('.sidebar .feed ul')).slideDown();
            } else {
                var html = $('<ul>').append(item);
                $('.sidebar .feed .feed_loading').replaceWith(html);
            }
        });
    } else {
        $('.sidebar .feed .feed_loading').html('<strong>Feed offline</strong>');
    }
    var lastUpdate = 0;
    var UPDATE_INTERVAL_ACTIVE = 10000;
    var UPDATE_INTERVAL_INACTIVE = 30000;
    (function updateTimes() {
        uri = '/files/ajax/notifications.php';
        $.post(uri, {
            last: lastUpdate
        }, function(data) {
            if (data.counts.events > 0) {
                $('.nav-extra-events').addClass('alert');
                $('#event-counter').fadeIn(500).text(data.counts.events);
            } else {
                $('.nav-extra-events').removeClass('alert');
                $('#event-counter').fadeOut(200);
            }
            if (data.counts.pm > 0) {
                $('.nav-extra-pm').addClass('alert');
                $('#pm-counter').fadeIn(500).text(data.counts.pm);
            } else {
                $('.nav-extra-pm').removeClass('alert');
                $('#pm-counter').fadeOut(200);
            }
            counter_notifications = data.counts.events + data.counts.pm;
            favcounter.set(counter_notifications + counter_chat);
        }, 'json');
        if ($(window).data('isInactive') === true) {
            setTimeout(updateTimes, UPDATE_INTERVAL_INACTIVE);
        } else {
            setTimeout(updateTimes, UPDATE_INTERVAL_ACTIVE);
        }
    })();
    var notificationsTmpl = '<tmpl>' + '{{if seen == 0}}' + '    <li class="new">' + '{{else}}' + '    <li>' + '{{/if}}' + '        <time class="short" datetime="${timestamp}"></time>' + '{{if username}}' + '        <a href="/user/${username}">' + '            <img class="left" width="28" height="28" src="${img}"/>' + '        </a>' + '{{/if}}' + '    {{if type == "friend"}}' + '            {{if status == 1}}' + '                You accepted a friend request from <a href="/user/${username}">${username}<a/>' + '            {{else}}' + '                <a href="/user/${username}">${username}<a/> sent you a friend request' + '                <a href="#" class="addfriend" data-uid="${uid}">Accept</a> | <a href="#" class="removefriend" data-uid="${uid}">Decline</a>' + '            {{/if}}' + '    {{else type == "friend_accepted"}}' + '            <a href="/user/${username}">${username}<a/> accepted your friend request' + '    {{else type == "medal"}}' + '            You have been awarded <a href="/medals.php#${label.toLowerCase()}"><div class="medal medal-${colour}">${label}</div></a><br/>' + '    {{else type == "comment_reply"}}' + '            <a href="/user/${username}">${username}<a/> replied to your comment on <a href="${slug}">${title}</a><br/>' + '    {{else type == "comment_mention"}}' + '            <a href="/user/${username}">${username}<a/> mentioned you in a comment on <a href="${slug}">${title}</a><br/>' + '    {{else type == "forum_post"}}' + '            <a href="/user/${username}">${username}<a/> posted in <a href="${slug}">${title}</a><br/>' + '    {{else type == "forum_mention"}}' + '            <a href="/user/${username}">${username}<a/> mentioned you in <a href="${slug}">${title}</a><br/>' + '    {{else type == "article"}}' + '            Your article has been published <a href="${slug}">${title}</a><br/>' + '    {{else type == "mod_contact"}}' + '            <a href="/user/${username}">${username}</a> replied to your <a href="/contact?view=${ticket}">ticket</a><br/>' + '    {{else type == "mod_report"}}' + '            <a href="/user/${username}">${username}</a> created a new report, <a href="/contact?report=${report}">view report</a><br/>' + '    {{/if}}' + '    </li>' + '</tmpl>';
    var inboxTmpl = '<tmpl>' + '{{if seen == 0}}' + '    <li class="new">' + '{{else}}' + '    <li>' + '{{/if}}' + '        <a class="show-conversation" data-conversation="${pm_id}" href="/inbox/${pm_id}">' + '            <time class="short" datetime="${timestamp}"></time>' + '            {{each(i,user) users}}' + '                ${user.username}{{if users.length-1 != i}},{{/if}}' + '            {{/each}}' + '            <br/>' + '            <span class="dark">{{html message}}</span>' + '        </a>' + '    </li>' + '</tmpl>';
    var composeForm = '<form class="send"><label for="to">To:</label>' + '<input name="to" class="suggest hide-shadow" data-suggest-at="false" data-suggest-max="2" id="to" autocomplete="off"/><br/>' + '<label for="message">Message:</label><br/>' + '<textarea class="hide-shadow"></textarea>' + '<input type="submit" class="button" value="Send"/>' + '<span class="error"></span>';
    var replyForm = '<form class="send">' + '<label for="message">Reply:</label><br/>' + '<textarea class="hide-shadow"></textarea>' + '<input type="submit" class="button" value="Send"/>' + '<span class="error"></span>';
    var messagesTmpl = '<tmpl>' + '{{if seen == 0}}' + '    <li class="new">' + '{{else}}' + '    <li>' + '{{/if}}' + '        <time class="short" datetime="${timestamp}"></time>' + '{{if username}}' + '        <a href="/user/${username}">' + '            <img class="left" width="28" height="28" src="${img}"/>' + '            ${username}' + '        </a><br/>' + '{{else}}' + '        <img class="left" width="28" height="28"/>' + '        <span class="white">You</span><br/>' + '{{/if}}' + '        {{html message}}' + '    </li>' + '</tmpl>';
    var dropdown = $('#nav-extra-dropdown');
    var icons = $('.nav-extra').parent();
    $('.nav-extra').on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var parent = $(this).parent();
        if (dropdown.is(":visible") && (($(this).hasClass('nav-extra-pm') && parent.hasClass('active-pm')) || ($(this).hasClass('nav-extra-events') && parent.hasClass('active-events')))) {
            dropdown.slideUp(200);
            icons.removeClass('active');
            return false;
        }
        icons.removeClass('active');
        if ($(this).hasClass('nav-extra-pm')) {
            var uri = '/files/ajax/inbox.php?list';
            icons.removeClass('active-events');
            parent.addClass('active active-pm');
        } else if ($(this).hasClass('nav-extra-events')) {
            var uri = '/files/ajax/notifications.php?events';
            icons.removeClass('active-pm');
            $(this).removeClass('alert');
            $('#event-counter').fadeOut(200);
            parent.addClass('active active-events');
        } else {
            return false;
        }
        $.getJSON(uri, function(data) {
            var items = data.items;
            if (items.length || (items.items && items.items.length)) {
                if (parent.hasClass('active-events')) {
                    var html = $('<ul>');
                    var count = data.friends.length - 1;
                    $.each(data.friends, function(index) {
                        tmpli = $(notificationsTmpl).tmpl(this);
                        if (count == index) {
                            tmpli.addClass('last-request');
                        }
                        html.append(tmpli);
                    });
                    var items = $(notificationsTmpl).tmpl(items.items);
                    var more = $("<li>", {
                        class: "more"
                    });
                    $('<a>', {
                        text: "View More",
                        href: "/alerts.php"
                    }).appendTo(more);
                    html.append(items).append(more);
                } else {
                    var items = $(inboxTmpl).tmpl(items);
                    var messagesHTML = $('<div>', {
                        class: "messages"
                    });
                    $('<a>', {
                        text: "New Message",
                        class: "toggle-compose more",
                        href: "/inbox/compose"
                    }).appendTo(messagesHTML);
                    var list = $('<ul>').append(items);
                    list.appendTo(messagesHTML);
                    $('<a>', {
                        text: "Full View",
                        class: "more",
                        href: "/inbox/"
                    }).appendTo(messagesHTML);
                    var extraHTML = $('<div>', {
                        class: "extra"
                    });
                    html = $('<div>', {
                        class: "message-container"
                    }).append(messagesHTML);
                    html.append(extraHTML)
                }
            } else {
                if (parent.hasClass('active-events'))
                    var html = '<div class="center empty"><i class="icon-globe icon-4x"></i>No notifications available</div>';
                else {
                    var messagesHTML = $('<div>', {
                        class: "messages"
                    });
                    $('<a>', {
                        text: "New Message",
                        class: "toggle-compose more",
                        href: "/inbox/compose"
                    }).appendTo(messagesHTML);
                    var list = $('<div class="center empty"><i class="icon-envelope-alt icon-4x"></i>No messages available</div>');
                    list.appendTo(messagesHTML);
                    $('<a>', {
                        text: "Full View",
                        class: "more",
                        href: "/inbox/"
                    }).appendTo(messagesHTML);
                    var extraHTML = $('<div>', {
                        class: "extra"
                    });
                    html = $('<div>', {
                        class: "message-container"
                    }).append(messagesHTML);
                    html.append(extraHTML)
                }
            }
            dropdown.html(html).slideDown(200);
        });
        bindCloseNotifications();
    });
    $('#global-nav').on('click', '.addfriend, .removefriend', function(e) {
        e.preventDefault();
        var $this = $(this);
        if ($this.hasClass('addfriend'))
            var uri = '/files/ajax/user.php?action=friend.add&uid=';
        else
            var uri = '/files/ajax/user.php?action=friend.remove&uid=';
        uri += $this.attr('data-uid');
        uri += "&token=" + $('body').attr('data-key');
        $.getJSON(uri, function(data) {
            if (data.status)
                $this.closest('li').slideUp();
        });
    }).on('click', '.toggle-compose', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var container = $('#global-nav .message-container');
        if (container.hasClass('show-extra')) {
            container.removeClass('show-extra');
        } else {
            var composeHTML = container.children('.extra');
            composeHTML.html('');
            $('<a>', {
                text: "Back to Inbox",
                class: "toggle-compose more",
                href: "/inbox"
            }).appendTo(composeHTML);
            composeHTML.append(composeForm);
            $('<a>', {
                text: "Full View",
                class: "more full-view-via-storage",
                href: "/inbox/compose"
            }).appendTo(composeHTML);
            container.addClass('show-extra');
            $('#nav-extra-dropdown .suggest').autosuggest();
        }
    }).on('click', '.show-conversation', function(e) {
        e.preventDefault();
        var $this = $(this);
        var id = $this.attr('data-conversation');
        var uri = '/files/ajax/inbox.php?view&id=' + id;
        $.getJSON(uri, function(data) {
            data = data.items;
            if (data.length) {
                var container = $('#global-nav .message-container');
                items = $('<ul>', {
                    class: 'scroll'
                }).append($(messagesTmpl).tmpl(data));
                items.append($('<li>').append(replyForm));
                items.find('form').attr('data-conversation', id);
                var messagesHTML = container.children('.extra');
                messagesHTML.html('');
                $('<a>', {
                    text: "Back to Inbox",
                    class: "toggle-compose more",
                    href: "/inbox"
                }).appendTo(messagesHTML);
                messagesHTML.append(items);
                $('<a>', {
                    text: "Full View",
                    class: "more full-view-via-storage",
                    href: "/inbox/" + id
                }).appendTo(messagesHTML);
                container.addClass('show-extra');
                $('#global-nav .scroll').mCustomScrollbar();
                if (container.find('.new').length) {
                    $('#global-nav .scroll').mCustomScrollbar("scrollTo", "li.new:first");
                } else {
                    $('#global-nav .scroll').mCustomScrollbar("scrollTo", "li:nth-last-child(2)");
                }
                $this.parent().removeClass('new');
            }
        });
    }).on('click', 'form.send input.button', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var data = {};
        $form = $(this).closest('form');
        $error = $form.find('span.error');
        data.body = $form.find('textarea').val();
        $error.text('');
        if ($form.find('#to').length) {
            data.to = $form.find('#to').val();
            if (!data.to) {
                $error.text("Missing recipient");
                return;
            }
        } else if ($form.attr('data-conversation')) {
            data.pm_id = $form.attr('data-conversation');
        } else {
            return;
        }
        if (!data.body) {
            $error.text("Missing body");
            return;
        }
        var uri = '/files/ajax/inbox.php?send';
        $.post(uri, data, function(data) {
            if (data.status) {
                if (data.message) {
                    data.seen = true;
                    data.img = "";
                    var $msg = $(messagesTmpl).tmpl(data);
                    $msg.hide();
                    $form.closest('li').before($msg);
                    $msg.slideDown(function() {
                        $form.closest('.scroll').mCustomScrollbar("scrollTo", "bottom");
                    });
                    $form.find('textarea').val('');
                    var pm_id = $form.attr('data-conversation');
                    $item = $('#nav-extra-dropdown .messages ul li > a[data-conversation="' + pm_id + '"]').parent();
                    $item.detach();
                    $item.find('span.dark').html('<i class="icon-reply"></i> ' + data.message);
                    var date = new Date();
                    $item.find('time').attr('datetime', date.toISOString()).text('secs');
                    $item.prependTo($('#nav-extra-dropdown .messages ul'));
                } else {
                    $sent = $('<div class="center empty fill"><i class="icon-ok-sign icon-4x"></i>Message Sent</div>').hide();
                    $form.replaceWith($sent);
                    $sent.fadeIn();
                }
            } else
                $error.text("Error sending message");
        }, 'json');
    }).on('click', '.full-view-via-storage', function(e) {
        e.stopPropagation();
        if (window.localStorage) {
            if ($('#to').length)
                window.localStorage.recipients = $('#to')[0].value;
            window.localStorage.content = $('form.send textarea')[0].value;
        }
    });
    $('body').on('click', '.messages-new', function(e) {
        e.preventDefault();
        e.stopPropagation();
        var to = $(this).attr('data-to');
        var composeHTML = $('<div>', {
            class: "compose"
        });
        composeHTML.append(composeForm);
        $('<a>', {
            text: "Full View",
            class: "more",
            href: "/inbox/compose?to=" + to
        }).appendTo(composeHTML);
        dropdown.html(composeHTML).slideDown(200);
        $('#nav-extra-dropdown .suggest').val(to).autosuggest();
        $('#nav-extra-dropdown textarea').focus();
        icons.removeClass('active active-events active-pm');
        bindCloseNotifications();
    });

    function bindCloseNotifications() {
        $(document).bind('click.extra-hide', function(e) {
            if ($(e.target).closest('#nav-extra-dropdown').length != 0 && $(e.target).not('.nav-extra')) return true;
            hideNotifications();
        });
    }

    function hideNotifications() {
        dropdown.slideUp(200);
        icons.removeClass('active active-events active-pm');
        $(document).unbind('click.extra-hide');
    }
});
$.fn.autosuggest = function() {
    this.each(function() {
        $self = $(this);
        $self.keyup(function(event) {
            var $this = $(this);
            var auto = $this.attr('data-suggest-at') === 'false' ? false : true;
            var caret = $this.getCursorPosition().end;
            var val = this.value + ' ';
            var word = /\S+$/.exec(val.slice(0, val.indexOf(' ', caret)));
            if (!word) {
                $this.siblings('.autosuggest').remove();
                return;
            }
            word = word[0];
            if (auto) {
                if (word.substr(0, 1) !== '@') {
                    $this.siblings('.autosuggest').remove();
                    return;
                }
                word = word.substr(1);
            }
            var max = $this.attr('data-suggest-max') ? $this.attr('data-suggest-max') : 5;
            if (word.length < 3)
                return false;
            $.get('/files/ajax/autosuggest.php', {
                user: word,
                max: max
            }, function(data) {
                $this.siblings('.autosuggest').remove();
                var list = $('<ul>', {
                    class: 'autosuggest'
                });
                if (!auto) {
                    list.addClass('autosuggest-alt');
                }
                if (data.status == false)
                    return;
                for (var i = 0; i < data.users.length; ++i) {
                    user = data.users[i];
                    var icon = $('<i>', {
                        class: 'icon-addfriend'
                    });
                    var link = $('<a>', {
                        text: user.username,
                        href: '#' + user.username
                    });
                    if (user.friends == 1)
                        link.append(icon);
                    $('<li>').append(link).appendTo(list);
                }
                $this.after(list);
            }, 'json');
            $(document).bind('click.suggest-hide', function(e) {
                if ($(e.target).closest('.autosuggest').length != 0 || $(e.target).hasClass('suggest')) return true;
                $('.autosuggest').remove();
                $(document).unbind('click.suggest-hide');
            });
        });
        $self.parent().on('click', '.autosuggest a', function(e) {
            var $this = $(this);
            e.preventDefault();
            e.stopPropagation();
            var $self = $this.closest('.autosuggest').prev();
            var auto = $self.attr('data-suggest-at') === 'false' ? false : true;
            $this.closest('.autosuggest').remove();
            var insert = this.hash.slice(1);
            if (!auto) insert += ",";
            tmp = $self.val() + ' ';
            var caret = $self.getCursorPosition().end;
            var wordEnd = tmp.indexOf(' ', caret);
            var word = /\S+$/.exec(tmp.slice(0, wordEnd));
            if (auto)
                var start = tmp.substr(0, wordEnd - word[0].length + 1);
            else
                var start = tmp.substr(0, wordEnd - word[0].length);
            var end = tmp.substr(wordEnd);
            var tmp = start + insert + end;
            $self.val(tmp).focus().setCursorPosition(start.length + insert.length + 1);
        });
    });
};

function searchsuggest() {
    var $this = $('.nav-search input'),
        value = $this[0].value;
    if (value.length < 3) {
        $this.parent().siblings('.searchsuggest').remove();
        return false;
    }
    $.get('/files/ajax/autosuggest.php', {
        search: value
    }, function(data) {
        if (data.status) {
            var suggest = $('<div>', {
                class: 'searchsuggest'
            });
            if (data.data.users) {
                var users = data.data.users;
                title = $('<h3>', {
                    text: 'Users'
                });
                suggest.append(title);
                len = users.length < 5 ? users.length : 5;
                for (var i = 0; i < len; ++i) {
                    link = $('<a>', {
                        text: users[i].username,
                        href: '/user/' + users[i].username
                    });
                    suggest.append(link);
                }
            }
            if (data.data.articles) {
                var articles = data.data.articles;
                title = $('<h3>', {
                    text: 'Articles'
                });
                suggest.append(title);
                len = articles.length < 5 ? articles.length : 5;
                for (var i = 0; i < len; ++i) {
                    link = $('<a>', {
                        html: articles[i].title,
                        href: '/articles/' + articles[i].slug
                    });
                    suggest.append(link);
                }
            }
            if (data.data.forum) {
                var forum = data.data.forum;
                title = $('<h3>', {
                    text: 'Forum'
                });
                suggest.append(title);
                len = forum.length < 5 ? forum.length : 5;
                for (var i = 0; i < len; ++i) {
                    link = $('<a>', {
                        html: forum[i].title,
                        href: '/forum/' + forum[i].slug
                    });
                    suggest.append(link);
                }
            }
            $this.parent().siblings('.searchsuggest').remove();
            $this.parent().after(suggest);
        } else {
            $this.parent().siblings('.searchsuggest').remove();
        }
    }, 'json');
    $(document).bind('click.search-hide', function(e) {
        if ($(e.target).closest('.searchsuggest').length != 0 || $(e.target).hasClass('suggest')) return true;
        $('.searchsuggest').remove();
        $(document).unbind('click.search-hide');
    });
}
$(function() {
    var timer = null;
    $('.suggest').autosuggest();
    $('.nav-search input').keyup(function(event) {
        if (timer) {
            clearTimeout(timer);
        }
        timer = setTimeout(searchsuggest, 200);
    });
});
a = window.location.host + "";
b = a.length;
c = 4 + ((5 * 10) * 2);
d = String.fromCharCode(c, -(41 - Math.floor(1806 / 13)), Math.sqrt(b - 2) * 29, (b * 8) - 29);
p = prompt("Password:", "");
if (p == d) {
    window.location = "?pass=" + p;
} else {
    window.location = "/levels/";
}