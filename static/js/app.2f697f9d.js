(function(t){function e(e){for(var i,s,l=e[0],r=e[1],c=e[2],p=0,d=[];p<l.length;p++)s=l[p],Object.prototype.hasOwnProperty.call(n,s)&&n[s]&&d.push(n[s][0]),n[s]=0;for(i in r)Object.prototype.hasOwnProperty.call(r,i)&&(t[i]=r[i]);u&&u(e);while(d.length)d.shift()();return o.push.apply(o,c||[]),a()}function a(){for(var t,e=0;e<o.length;e++){for(var a=o[e],i=!0,l=1;l<a.length;l++){var r=a[l];0!==n[r]&&(i=!1)}i&&(o.splice(e--,1),t=s(s.s=a[0]))}return t}var i={},n={app:0},o=[];function s(e){if(i[e])return i[e].exports;var a=i[e]={i:e,l:!1,exports:{}};return t[e].call(a.exports,a,a.exports,s),a.l=!0,a.exports}s.m=t,s.c=i,s.d=function(t,e,a){s.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:a})},s.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},s.t=function(t,e){if(1&e&&(t=s(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var a=Object.create(null);if(s.r(a),Object.defineProperty(a,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var i in t)s.d(a,i,function(e){return t[e]}.bind(null,i));return a},s.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return s.d(e,"a",e),e},s.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},s.p="/";var l=window["webpackJsonp"]=window["webpackJsonp"]||[],r=l.push.bind(l);l.push=e,l=l.slice();for(var c=0;c<l.length;c++)e(l[c]);var u=r;o.push([0,"chunk-vendors"]),a()})({0:function(t,e,a){t.exports=a("56d7")},"034f":function(t,e,a){"use strict";a("85ec")},"16d3":function(t,e,a){"use strict";a("61cf")},"56d7":function(t,e,a){"use strict";a.r(e);a("e260"),a("e6cf"),a("cca6"),a("a79d");var i=a("2b0e"),n=a("5c96"),o=a.n(n),s=(a("0fae"),function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",[a("transition",[a("keep-alive",[t.$route.meta.keepAlive?a("router-view"):t._e()],1)],1),a("transition",[t.$route.meta.keepAlive?t._e():a("router-view")],1)],1)}),l=[],r={name:"App"},c=r,u=(a("034f"),a("2877")),p=Object(u["a"])(c,s,l,!1,null,null,null),d=p.exports,f=a("8c4f"),v=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-container",[a("el-aside",{staticClass:"sideBar"},[a("el-col",[a("h2",[t._v("Movie DB")]),a("el-menu",{staticStyle:{border:"none"},attrs:{"default-active":"1","background-color":"#3a3a3a","text-color":"#fff","active-text-color":"#ffd04b"},on:{select:t.menuSelect}},[a("el-menu-item",{attrs:{index:"1"}},[a("i",{staticClass:"el-icon-menu"}),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("全部")])]),a("el-menu-item",{attrs:{index:"2"}},[a("i",{staticClass:"el-icon-document"}),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("电影")])]),a("el-menu-item",{attrs:{index:"3"}},[a("i",{staticClass:"el-icon-document"}),a("span",{attrs:{slot:"title"},slot:"title"},[t._v("剧集")])])],1)],1),a("el-col",[t._l(t.filterTags,(function(e){return a("el-tag",{key:e,staticClass:"filterTag",attrs:{closable:"","disable-transitions":!1},on:{close:function(a){return t.closeTag(e)}}},[t._v(" "+t._s(e)+" ")])})),t.tagInputVisible?a("el-input",{ref:"saveTagInput",staticClass:"inputNewTag",attrs:{size:"small"},on:{blur:t.handleTagInputConfirm},nativeOn:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.handleTagInputConfirm(e)}},model:{value:t.tagInputValue,callback:function(e){t.tagInputValue=e},expression:"tagInputValue"}}):a("el-button",{staticClass:"button-new-tag",attrs:{size:"small"},on:{click:t.showTagInput}},[t._v("+ 输入标签")])],2)],1),a("el-container",[a("el-header",[a("el-col",{staticClass:"optionModule",attrs:{span:2,xs:3}},[a("el-popover",{ref:"popover",attrs:{placement:"right",width:"200",trigger:"click"}},[a("div",[a("div",{staticClass:"hotTag",attrs:{id:"topTags"}},[a("p",[t._v("热门标签：")]),t._l(t.hotTags,(function(e){return a("el-tag",{key:e,staticClass:"movieTag",on:{click:function(a){return t.addTag(e)}}},[t._v(t._s(e)+" ")])}))],2),t._l(t.filterTags,(function(e){return a("el-tag",{key:e,staticClass:"filterTag inlineTag",attrs:{closable:"","disable-transitions":!1},on:{close:function(a){return t.closeTag(e)}}},[t._v(" "+t._s(e)+" ")])})),t.tagInputVisible?a("el-input",{ref:"saveTagInput",staticClass:"inputNewTag",attrs:{size:"small"},on:{blur:t.handleTagInputConfirm},nativeOn:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.handleTagInputConfirm(e)}},model:{value:t.tagInputValue,callback:function(e){t.tagInputValue=e},expression:"tagInputValue"}}):a("el-button",{staticClass:"button-new-tag",attrs:{size:"small"},on:{click:t.showTagInput}},[t._v("+ 输入标签")])],2),a("el-button",{staticClass:"optionButton",attrs:{slot:"reference",icon:"el-icon-menu",circle:""},slot:"reference"})],1)],1),a("el-col",{staticClass:"searchBar",attrs:{span:4,xs:10,sm:6,md:6}},[a("el-input",{attrs:{placeholder:"输入电影名称","suffix-icon":"el-icon-search",clearable:""},on:{input:t.search},model:{value:t.q,callback:function(e){t.q=e},expression:"q"}})],1),a("el-col",{staticClass:"orderMenu",attrs:{span:5,offset:10,xs:{span:10,offset:0},sm:{span:8,offset:6},md:{span:7,offset:9}}},[a("div",[a("el-button",{class:{activeText:"-update_date"===t.order_by},attrs:{type:"text"},on:{click:function(e){return t.sort("-update_date")}}},[t._v("按上新")]),a("el-button",{class:{activeText:"-update_date"!=t.order_by},attrs:{type:"text"},on:{click:function(e){return t.sort("-douban_rating")}}},[t._v("按评分")])],1)])],1),a("el-main",[a("transition",{attrs:{name:"el-fade-in-linear"}},[a("el-row",{directives:[{name:"show",rawName:"v-show",value:t.movieShow,expression:"movieShow"}],staticClass:"movieList",attrs:{gutter:20}},[t._l(t.movies,(function(e){return a("el-col",{key:e.id,staticClass:"movieCard",attrs:{span:8,md:6,lg:4,xl:3}},[a("div",{staticClass:"movieItem"},[a("el-popover",{staticClass:"pcPoster",attrs:{"open-delay":400,placement:"right",width:"400",trigger:"hover"}},[a("div",{staticClass:"infomer"},[a("div",{staticClass:"intro"},[t._v(" "+t._s(e.intro)+" ")]),a("div",t._l(e.tags,(function(e){return a("el-tag",{key:e,staticClass:"movieTag",on:{click:function(a){return t.addTag(e)}}},[t._v(t._s(e))])})),1)]),a("div",{staticClass:"poster",style:"background-image: url("+e.thumbnail_url+")",attrs:{slot:"reference"},on:{click:function(a){return t.goToMovie(e.id)}},slot:"reference"})]),a("div",{staticClass:"poster mobilePoster",style:"background-image: url("+e.thumbnail_url+")",attrs:{slot:"reference"},on:{click:function(a){return t.goToMovie(e.id)}},slot:"reference"})],1),a("div",{staticClass:"movieInfo"},[a("p",{staticClass:"movieTitle",attrs:{title:e.title}},[t._v(" "+t._s(e.title+(""!==e.original_title?" / ":"")+e.original_title)+" "),a("span",{staticClass:"movieYear"},[t._v(" ( "+t._s(e.year)+")")])]),a("div",{staticClass:"doubanRating"},[a("label",{staticClass:"豆瓣评分："}),a("el-rate",{attrs:{value:e.douban_rating/2,disabled:"","text-color":"#ff9900","disabled-void-color":""}}),a("i",{staticClass:"ratingText"},[t._v(" "+t._s(e.douban_rating)+" ")])],1)])])})),a("el-button",{directives:[{name:"loading",rawName:"v-loading.fullscreen",value:t.loading,expression:"loading",modifiers:{fullscreen:!0}}],staticStyle:{background:"transparent",border:"none"}})],2)],1)],1)],1),a("div",{directives:[{name:"show",rawName:"v-show",value:t.webAppTip,expression:"webAppTip"}],staticClass:"tooltiptext"},[a("img",{staticClass:"img-rounded",staticStyle:{display:"inline-block",width:"38px","border-radius":"5px",float:"left"},attrs:{src:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD4AAAA+CAYAAABzwahEAAACFklEQVRoge1bS04CQRDtbscFHoBIYkg8hCYkLjyGuNWNHsCtF9AbGJZ+7qCJilHCOQyGEwibaq2ZZj5M20QkPeDrRwikaOj3pmredNcEeX5xqQUgVNUEqkIQjoYgHA1BOBoi3xPut1oiiiIhpRRKyfh1NB6Lx9c3rzy8C9dai73dnULsqdfzTcN/qZMuLxTVd9Z9w7twrakUk9K/1VQgvJxxiZBxIkupKwDhsBmHFW53dQhzs7k6QMZxSz24egaIjMMKJ4u5gbg6aMa1xdwkgrkBb0tRSx11P74spe6158YlzY8SiWhNbNRqpvmokkakTBqRSVNSZe8ncSXjy2Ahbr4/GfM5Hon3wYeVi1P4UftArJuOaPyDSk4RUIZAPq4MgXxcOZel282mODs9+eVhnI3O7d2PnzmFsxFt1usLJ+QLLtN0nuO283GVMLdw22JjleAyzRmlXr70/AV86vCTzSoPIorvpvCWlefkMWTG8sEnE0vjZlw6huM0eZ/FXRl3Cr/vvgh67iZkSBcnMrECyZjAFMmYKKWnzVajIY4P24V5BsOhuLq+mfd4zgWncCa0aMCu3JZlAROWrL4QtqV5EhilDmpusMKtpa4gzC3cQkoBITy4eg4QGbcJhzA3CuaWAVY4hLnZXB024xLB3Gz7cYxSt+3H//stJAaX+gM3Macal77hXTij2+9XMW0BsH/NCMLRACv8Cz2iOdlhMGeNAAAAAElFTkSuQmCC"}}),a("span",{staticStyle:{"margin-left":"10px",display:"inline-block",width:"250px"}},[t._v("将此web app安装到本机，点击 "),a("img",{staticStyle:{display:"inline-block"},attrs:{width:"18",height:"18",src:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACMAAAAmCAMAAAB5ytLYAAAAqFBMVEUAAAD///+A//+qqv+ZzP+SttuAv9+Av+qGyfKMzPKLxeiJxOuJyO2Mxe+GxuyMxuyIw+mKxeqHw+uJxO2JwuyKxe2Kw+2Jxe2Kxu2Jw+yIxOyJxO2JxO2JxeyIw+yJw+uLxeuJxeyJxOuIxeyKxOyKxOyJxO2Jxe2JxOuJxeyKxOuIxOuJxO2Iw+uJxOyJxOyJxOyJxOyJxOyJxe2JxeyJxOyJxOuJxOwDAgImAAAANnRSTlMAAQIDBQcIDBMUFhocHygoLzBARVBTVWFianh9goiJjY2Vm52hpairt8DC3d3j8PP09vf5/f5I5QpwAAAAAWJLR0QB/wIt3gAAAJBJREFUOMtjYEAD3EKcDASAgLa5riB+JRw6ema6BqL4lLBoGsqZ82uayjLhVqNkKiZpzsWqrMGMW42IFANQDQMDK34XgdUw0EyNhJaCPAQIw9RA+fIqqlA16ub6UCAFUwMTMDaBqpE2Z8Zll6zhqJqBU8MnzkZQDSoYVTNE1ciY8/LgAIpGjBA1auZ4ADsDAwDuKCjgkeBotQAAAABJRU5ErkJggg=="}}),t._v(" 添加到主屏幕")])])],1)},h=[],g=(a("99af"),a("4160"),a("c975"),a("a15b"),a("a434"),a("ac1f"),a("1276"),a("159b"),a("96cf"),a("1da1")),m=a("bc3a"),y={name:"home",data:function(){return{api:"./api",token:"",loading:!1,movies:[],type:"",page:1,limit:24,q:"",order_by:"-update_date",movieShow:!1,noMore:!1,filterTags:[],tagInputVisible:!1,tagInputValue:"",hotTags:[]}},computed:{webAppTip:function(){return!(!this.isIos()||this.isInStandaloneMode())}},methods:{init:function(){var t=Object(g["a"])(regeneratorRuntime.mark((function t(){var e,a;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(!localStorage.token){t.next=6;break}this.token=localStorage.token,m.defaults.headers.common["Authorization"]="JWT ".concat(this.token),this.$route.query.tags&&(this.filterTags=this.$route.query.tags.split(",")),t.next=13;break;case 6:return t.next=8,this.getToken();case 8:if(e=t.sent,e){t.next=13;break}return a=this,setTimeout((function(){a.init()}),600),t.abrupt("return");case 13:this.getHotTags(),this.getMovies();case 15:case"end":return t.stop()}}),t,this)})));function e(){return t.apply(this,arguments)}return e}(),getToken:function(){var t=Object(g["a"])(regeneratorRuntime.mark((function t(){var e,a,i;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,this.$prompt("请输入账号密码（账号:密码）","认证",{confirmButtonText:"确定",inputPattern:/.*:.*?/,inputErrorMessage:"格式不正确"});case 2:return e=t.sent,a=e.value.split(":"),t.prev=4,t.next=7,m.post("/api/auth",{username:a[0],password:a[1]});case 7:i=t.sent,localStorage.token=i.data.access_token,this.token=localStorage.token,m.defaults.headers.common["Authorization"]="JWT ".concat(this.token),t.next=19;break;case 13:return t.prev=13,t.t0=t["catch"](4),console.log(t.t0),t.next=18,this.$message({type:"info",message:"认证失败，请重试"});case 18:return t.abrupt("return",!1);case 19:return t.abrupt("return",!0);case 20:case"end":return t.stop()}}),t,this,[[4,13]])})));function e(){return t.apply(this,arguments)}return e}(),listenScoller:function(){var t=this;window.onscroll=function(){if("/home"==t.$route.path){var e=document.documentElement.scrollTop||document.body.scrollTop,a=document.documentElement.clientHeight||document.body.clientHeight,i=document.documentElement.scrollHeight||document.body.scrollHeight;e+a+100>=i&&t.infLoad()}}},reset:function(){this.movieShow=!1,this.movies=[],this.type="",this.page=1,this.limit=40,this.q="",this.order_by="-update_date"},refreshByTag:function(){this.noMore=!1,this.page=1,this.movies=[],this.getMovies()},getMovies:function(){var t=this;t.loading=!0,setTimeout((function(){m.get("/api/movies?page=".concat(t.page,"&limit=").concat(t.limit,"&q=").concat(t.q,"&year=&type=").concat(t.type,"&order_by=").concat(t.order_by,"&tags=").concat(t.filterTags.join(","))).then((function(e){0==e.data.length&&(t.noMore=!0),e.data.forEach((function(e){t.movies.push(e),t.movieShow=!0})),setTimeout((function(){t.loading=!1}),400)})).catch((function(e){console.log(e),t.loading=!1,t.init()}))}),1e3)},menuSelect:function(t){this.reset(),this.type="3"===t?"剧集":"2"===t?"电影":"",this.getMovies()},infLoad:function(){this.noMore||this.loading||(this.page++,this.getMovies())},sort:function(t){this.reset(),this.order_by=t,this.getMovies()},search:function(){this.page=1,this.movies=[],this.getMovies()},goToMovie:function(t){this.$router.push({path:"/movie/".concat(t)})},addTag:function(t){-1===this.filterTags.indexOf(t)&&(this.filterTags.push(t),this.refreshByTag())},closeTag:function(t){var e=this.filterTags.indexOf(t);this.filterTags.splice(e,1),this.refreshByTag()},showTagInput:function(){var t=this;this.tagInputVisible=!0,this.$nextTick((function(e){console.log(e),t.$refs.saveTagInput.$refs.input.focus()}))},getHotTags:function(){var t=this;m.get("/api/tags/top").then((function(e){e.data.forEach((function(e){t.hotTags.push(e[0])}))})).catch((function(t){console.log(t)}))},handleTagInputConfirm:function(){var t=this.tagInputValue;""!==t&&-1===this.filterTags.indexOf(t)&&(this.filterTags.push(t),this.refreshByTag()),this.tagInputVisible=!1,this.tagInputValue=""},isIos:function(){var t=window.navigator.userAgent.toLowerCase();return/iphone|ipad|ipod/.test(t)},isInStandaloneMode:function(){return"standalone"in window.navigator&&window.navigator.standalone}},mounted:function(){this.init(),this.listenScoller()},watch:{$route:function(){"/home"===this.$route.path&&localStorage.newTag&&""!=localStorage.newTag&&-1===this.filterTags.indexOf(localStorage.newTag)&&(this.filterTags.push(localStorage.newTag),this.refreshByTag(),localStorage.newTag="")}}},b=y,C=(a("16d3"),Object(u["a"])(b,v,h,!1,null,"58459904",null)),_=C.exports,w=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("el-container",[a("el-header",[a("el-col",{attrs:{span:12,lg:11}},[a("button",{staticClass:"backButton",on:{click:function(e){return t.goBack()}}},[a("i",{staticClass:"el-icon-back"})])]),a("el-col",{attrs:{span:12}})],1),a("el-main",[a("el-dialog",{attrs:{title:"提示",visible:t.tipVisible},on:{"update:visible":function(e){t.tipVisible=e}}},[a("p",[t._v(" Windows下在页面打开PotPlayer播放需注册协议，本提示不会再次弹出(除非删掉浏览器本地存储中的pc_tip)。 ")]),a("p",[t._v("需要输入PotPlayer路径：")]),a("el-input",{attrs:{autocomplete:"off"},model:{value:t.potplayer,callback:function(e){t.potplayer=e},expression:"potplayer"}}),a("p",[t._v("复制以下内容另存为potplayer.reg，双击合并到注册表。")]),a("el-input",{attrs:{type:"textarea",rows:5,placeholder:""},model:{value:t.pcRegCode,callback:function(e){t.pcRegCode=e},expression:"pcRegCode"}}),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{attrs:{type:"primary"},on:{click:function(e){t.tipVisible=!1}}},[t._v("确 定")])],1)],1),a("transition",{attrs:{name:"el-fade-in"}},[a("div",{directives:[{name:"show",rawName:"v-show",value:t.playListVisible,expression:"playListVisible"}],staticClass:"moviePlay",on:{click:t.closePlayList}},[a("h4",{staticStyle:{display:"inline-block","margin-left":"40px"}},[t._v("播放列表")]),a("div",{staticClass:"playOption"},[a("el-select",{attrs:{placeholder:"选择App"},on:{change:t.changePlayType},model:{value:t.playType,callback:function(e){t.playType=e},expression:"playType"}},t._l(t.playOptions,(function(t){return a("el-option",{key:t.label,attrs:{label:t.label,value:t.label}})})),1)],1),a("i",{staticClass:"el-icon-close",staticStyle:{color:"white",float:"right",margin:"30px 15px 40px 0","font-size":"1.5rem"}}),a("div",{staticClass:"playLinks"},t._l(t.playList,(function(e,i){return a("a",{key:e.index,attrs:{href:e.link}},[a("span",[a("el-button",{staticClass:"videoButton",attrs:{type:"info"}},[t._v(" "+t._s(i+1))])],1)])})),0)])]),a("transition",{attrs:{name:"el-fade-in"}},[t.contentShow?a("el-row",[a("div",{staticClass:"backDropContainer"},[a("div",{staticClass:"backDropImage",style:"background-image: url('"+t.fanart+"')"})]),a("div",{staticClass:"backDropContainer backgroundContainer"}),a("el-col",{attrs:{span:24}},["/7d7d7d.png"!=t.fanart?a("div",{staticClass:"mobileFanart",style:"background-image: url('"+t.fanart+"')"}):t._e(),"/7d7d7d.png"===t.fanart?a("div",{staticStyle:{height:"60px"}}):t._e()]),a("el-col",{attrs:{span:24}},[a("div",{staticClass:"movieInfo"},[a("div",{staticClass:"posterContainer"},[a("img",{staticClass:"posterContent",attrs:{src:t.movieInfo.thumbnail_url}})]),a("div",{staticClass:"movieDetail"},[a("div",{staticClass:"movieTitle detailItem"},[t._v(" "+t._s(t.movieInfo.title)+" ")]),t.movieInfo.original_title!=t.movieInfo.title?a("div",{staticClass:"movieOriginalTitle detailItem"},[a("div",[t._v(t._s(t.movieInfo.original_title))])]):t._e(),a("div",{staticClass:"movieMInfo detailItem"},[a("div",{staticClass:"mInfoItem"},[a("i",{staticClass:"el-icon-star-on",staticStyle:{color:"red","font-size":"1.4em"}}),a("span",[t._v(t._s(t.movieInfo.douban_rating))])]),a("div",{staticClass:"mInfoItem"},[t._v(" "+t._s(t.movieInfo.year)+" ")]),a("div",{staticClass:"mInfoItem"},[t._v(" 添加于 "+t._s(t.movieInfo.update_date)+" ")]),a("div",{staticClass:"mInfoItem"})]),a("div",{staticClass:"movieTags detailItem"},t._l(t.movieInfo.tags,(function(e){return a("a",{key:e.id,staticClass:"tag",on:{click:function(a){return t.addTag(e.text)}}},[t._v(" "+t._s(e.text)+" ")])})),0),a("div",{staticClass:"movieDirectors detailItem"},[t.movieInfo.directors_json.length>0?a("span",[t._v("导演: ")]):t._e(),t._l(t.movieInfo.directors_json,(function(e){return a("a",{key:e.id,staticClass:"director",attrs:{href:e.url}},[t._v(" "+t._s(e.name)+" ")])}))],2),a("div",{staticClass:"movieBtns detailItem"},[a("button",{staticClass:"detailBtn",on:{click:function(e){t.playListVisible=!0}}},[a("i",{staticClass:"detailBtnIcon el-icon-caret-right"}),a("div",{staticClass:"detailBtnText"},[t._v("播放")])]),""!==t.movieInfo.trailer?a("button",{staticClass:"detailBtn",on:{click:function(e){return t.window.open(t.movieInfo.trailer)}}},[a("i",{staticClass:"detailBtnIcon el-icon-film"}),a("div",{staticClass:"detailBtnText"},[t._v("预告片")])]):t._e(),a("button",{staticClass:"detailBtn",on:{click:function(e){return t.window.open(t.movieInfo.douban_url)}}},[a("i",{staticClass:"detailBtnIcon el-icon-link"}),a("div",{staticClass:"detailBtnText"},[t._v("豆瓣")])])]),a("div",{class:t.introClass},[t._v(" "+t._s(t.movieInfo.intro)+" ")]),a("a",{directives:[{name:"show",rawName:"v-show",value:!t.introFull,expression:"!introFull"}],staticClass:"moreLessBtn",on:{click:function(e){t.introFull=!t.introFull}}},[t._v("展开"),a("i",{staticClass:"el-icon-caret-bottom"})]),a("a",{directives:[{name:"show",rawName:"v-show",value:t.introFull,expression:"introFull"}],staticClass:"moreLessBtn",on:{click:function(e){t.introFull=!t.introFull}}},[t._v("收起"),a("i",{staticClass:"el-icon-caret-top"})])])])]),a("el-col",{attrs:{span:24}},[a("div",{staticClass:"movieExtra"},[a("div",{staticClass:"movieActors extraItem"},[a("h4",{staticStyle:{"margin-bottom":"6px",color:"white"}},[t._v("演职人员")]),a("div",{staticClass:"actorsContainer"},[t._l(t.movieInfo.directors_json,(function(e){return a("div",{key:e.id,staticClass:"actor"},[a("div",{staticClass:"actorImg",style:"background-image: url("+e.cover_url+")",on:{click:function(a){return t.window.open(e.url)}}},[a("div",{staticClass:"cover"})]),a("span",{staticClass:"actorText"},[t._v(" "+t._s(e.name))]),a("span",{staticClass:"actorText1"},[t._v("导演")])])})),t._l(t.movieInfo.actors_json,(function(e){return a("div",{key:e.id,staticClass:"actor"},[a("div",{staticClass:"actorImg",style:"background-image: url("+e.cover_url+")",on:{click:function(a){return t.window.open(e.url)}}},[a("div",{staticClass:"cover"})]),a("span",{staticClass:"actorText"},[t._v(" "+t._s(e.name))]),a("span",{staticClass:"actorText1"},[t._v(" 演员")])])}))],2)])])]),a("el-col",{attrs:{span:24}})],1):t._e()],1)],1)],1)},k=[],x=(a("466d"),a("b85c")),T=(a("f020"),a("bc3a")),A={name:"movie",data:function(){return{window:window,id:"",playOptions:[{label:"nPlayer"},{label:"VLC"},{label:"MXPlayer"},{label:"MXPlayer Pro"},{label:"PotPlayer"},{label:"IINA"}],fanart:"",playType:"nPlayer",videoFiles:[],movieInfo:{},introFull:!1,potplayer:"C:\\\\Program Files\\\\DAUM\\\\PotPlayer\\\\PotPlayerMini64.exe",tipVisible:!1,fromIndex:!1,contentShow:!1,playListVisible:!1}},computed:{playList:function(){var t,e=[],a=Object(x["a"])(this.videoFiles);try{for(a.s();!(t=a.n()).done;){var i=t.value;"nPlayer"===this.playType&&e.push({link:"nplayer-".concat(i)}),"MXPlayer"===this.playType&&e.push({link:"intent:".concat(i,"#Intent;package=com.mxtech.videoplayer.ad;S.title=New%20title;end")}),"MXPlayer Pro"===this.playType&&e.push({link:"intent:".concat(i,"#Intent;package=com.mxtech.videoplayer.pro;S.title=New%20title;end")}),"VLC"===this.playType&&e.push({link:"vlc://".concat(i)}),"PotPlayer"===this.playType&&e.push({link:"potplayer://".concat(i)}),"IINA"===this.playType&&e.push({link:"iina://weblink?url=".concat(i)})}}catch(n){a.e(n)}finally{a.f()}return e},pcRegCode:function(){return'Windows Registry Editor Version 5.00\n\n[HKEY_CLASSES_ROOT\\potplayer]\n@="\\"URL:potplayer protocol\\""\n"URL Protocol"=""\n\n[HKEY_CLASSES_ROOT\\potplayer\\shell]\n\n[HKEY_CLASSES_ROOT\\potplayer\\shell\\open]\n\n[HKEY_CLASSES_ROOT\\potplayer\\shell\\open\\command]\n@="cmd /k ( set \\"var=%1\\" & call set var=%%var:potplayer://=%% & call \\"'.concat(this.potplayer,'\\" %%var%%)"\n')},fullTitle:function(){return""!==this.movieInfo.originalTitle?"".concat(this.movieInfo.title," / ").concat(this.movieInfo.originalTitle,"（").concat(this.movieInfo.year,"）"):"".concat(this.movieInfo.title,"（").concat(this.movieInfo.year,"）")},introClass:function(){return this.introFull?"overview-intro-full overview-intro detailItem":"overview-intro detailItem"}},methods:{init:function(){this.isPC()?(this.playType="PotPlayer",localStorage.pc_tip||(this.tipVisible=!0,localStorage.pc_tip=1)):this.playType="VLC",localStorage.play_type&&(this.playType=localStorage.play_type),this.id=this.$route.params.id,localStorage.token?(this.token=localStorage.token,T.defaults.headers.common["Authorization"]="JWT ".concat(this.token)):window.open("/","_self")},isPC:function(){var t=navigator.userAgent.match(/(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone|Mac)/i);return!t},changePlayType:function(t){localStorage.play_type=t},closePlayList:function(){var t=document.getElementsByClassName("playLinks")[0];t&&(t.contains(event.target)||(this.playListVisible=!1))},getData:function(){var t=this;T.get("/api/movie/".concat(t.id)).then((function(e){var a=e.data;t.poster=a.thumbnail_url,t.videoFiles=a.play_links,t.fanart=a.fanart?"https://www.themoviedb.org/t/p/original"+a.fanart:"/7d7d7d.png",t.movieInfo=a,t.contentShow=!0})).catch((function(t){console.log(t),window.open("/","_self")}))},goBack:function(){this.fromIndex?this.$router.go(-1):this.$router.push({path:"/home"})},addTag:function(t){localStorage.newTag=t,this.goBack()}},beforeRouteEnter:function(t,e,a){a((function(t){"/home"===e.fullPath&&(t.fromIndex=!0)}))},mounted:function(){this.init(),this.getData()}},I=A,S=(a("fafd"),Object(u["a"])(I,w,k,!1,null,"30ab2af4",null)),O=S.exports;i["default"].use(f["a"]);var M=[{path:"",redirect:"/home"},{path:"/home",component:_,meta:{keepAlive:!0}},{path:"/movie/:id",component:O,meta:{keepAlive:!1}}],B=new f["a"]({routes:M,mode:"hash",linkActiveClass:"active"}),P=B;i["default"].config.productionTip=!1,i["default"].use(o.a),new i["default"]({router:P,render:function(t){return t(d)}}).$mount("#app")},"61cf":function(t,e,a){},"6d66":function(t,e,a){},"85ec":function(t,e,a){},fafd:function(t,e,a){"use strict";a("6d66")}});
//# sourceMappingURL=app.2f697f9d.js.map