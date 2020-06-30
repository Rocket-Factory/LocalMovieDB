$().ready(function () {
    main.init();
});

// let apiUrl = "./js/data.json"; //测试数据,部署时注释掉
let apiUrl = "/api/movies";//实际接口
let main = {
    orderBy: '',
    orderType: 'asc',

    queryYear: '',
    curPage: 1,
    queryTags: [],


    init: function () {
        main.initBtnEvent();
        main.initScrollEvent();

        main.getData();
    },
    getData: function (loading) {
        $('#moviesListContent').html('');
        main.curPage = 1;
        main.ajaxData(loading !== false);
    },
    ajaxData: function (enableLoading = false) {
        if (enableLoading === true) {
            loading()
        }
        let params = {
            page: main.curPage,
            limit: 20,
            q: $('#queryInput').val() || '',
            year: main.queryYear || '',
            tags: main.queryTags.join()
        };
        if (main.orderBy) {
            params.order_by = (main.orderType === "asc" ? "" : "-") + main.orderBy
        }

        $.ajax({
            url: apiUrl,
            type: "GET",
            data: params,
            success: function (data) {
                main.refreshMoviesContent(data);
            },
            error: function (e) {
                console.error(e);
                alert("请求失败！");
            },
            complete: function () {
                if (enableLoading === true) {
                    unloading()
                }
            }
        });
    },
    initBtnEvent: function () {
        $('.orderMenu li').off('click').on('click', function () {
            let beforeOrderType = $(this).find('.fa-long-arrow-down').length ? 'desc' : 'asc';
            $('.orderMenu li .fa').remove();
            $('.orderMenu li').removeClass('active');
            $(this).addClass('active');
            $(this).append('<i class="fa ' + (beforeOrderType === 'desc' ? 'fa-long-arrow-up' : 'fa-long-arrow-down') + '"></i>');

            main.orderBy = $(this).attr('value');
            main.orderType = beforeOrderType === 'desc' ? 'asc' : 'desc';
            main.getData();
            $('#orderMenu').hide();
        });

        $('.filterYears li').off('click').on('click', function () {
            $('.filterYears li').removeClass('active');
            $(this).addClass('active');
            $('#fixedFilterYears').hide();
            main.queryYear = $(this).attr('value');
            main.getData();
        });

        $('#searchBtn').off('click').on('click', function () {
            main.getData();
        });

        $('#queryInput').off('keyup').on('keyup', function (e) {
            if (e.keyCode === 13) {
                $('#searchBtn').click();
            }
        });

        $('#fixedLogo').off('click').on('click', function () {
            $('.sideMenu').animate({left: 0}, 'fast');
            $('body').off('click').on('click', function (e) {
                if (
                    !($(e.target).attr('id') === 'fixedLogo'
                        || $(e.target).hasClass('sideMenu')
                        || $(e.target).hasClass('filterContent')
                        // || $(e.target).hasClass('filterItem')
                        // || $(e.target).parent().hasClass('filterItem')
                        // || $(e.target).parent().hasClass('filterOptions')
                        || $(e.target).hasClass('filterItem')
                        || $(e.target).hasClass('filterOptions')
                    )
                ) {
                    $('.sideMenu').animate({left: '-250px'}, 'fast');
                    $('body').off('click');
                }
            })
        });

    },
    initScrollEvent: function () {
        $(window).scroll(function () {
            let scrollTop = parseInt(document.documentElement.scrollTop || document.body.scrollTop);
            let clientHeight = parseInt(document.documentElement.clientHeight || document.body.clientHeight);
            let scrollHeight = parseInt(document.documentElement.scrollHeight || document.body.scrollHeight);
            if (scrollHeight > clientHeight && (Math.abs(scrollTop + clientHeight - scrollHeight) < 5)) {
                main.curPage++;
                main.ajaxData();
            }
        });
        window.onresize = function () {
            if (parseInt(document.documentElement.clientWidth || document.body.clientWidth) > 1000) {
                $('.sideMenu').css({left: 0});
            } else {
                $('.sideMenu').css({left: '-250px'});
            }
        };
    },
    initTagEvent: function () {
        $('#moviesListContent .movieTag').off('click').on('click', function () {
            let curTag = $(this).text();
            if (main.queryTags.indexOf(curTag) === -1) {
                let $li = '<li class="tabOptions" data-tag="' + curTag + '">' + $(this).text() + '<i class="fa fa-times" onclick="main.removeTag(\'' + curTag + '\')" style="margin-left: 3px"></i></li>';
                $('#selectedTags').append($li);
                $('#menuSelectedTags').append($li);
                main.queryTags.push(curTag);
                main.getData(false);
            }
        });
    },
    removeTag: function (tag) {
        main.queryTags.splice(main.queryTags.indexOf(tag), 1);
        $('.tabOptions[data-tag="' + tag + '"]').remove();
        main.getData(false);
    },
    refreshMoviesContent: function (data) {
        let pre_uri = $("#configUri").attr("preUri");
        let after_uri = $("#configUri").attr("after_uri");
        let moviesHtml = '';
        if (data.length > 0) {
            data.forEach(function (item) {
                let tags = (item.tags || []).map(function (tag) {
                    return '<span class="movieTag">' + tag + '</span>'
                });
                moviesHtml +=
                    '<div class="movieItem">' +
                    '   <a href="' + item.douban_url + '"><img class="poster" src="' + item.thumbnail_url + '"></a>' +
                    '   <div class="movieInfo">' +
                    '       <p class="movieTitle" title="' + item.title + '">' +
                    item.title + (item.original_title !== item.title ? '&nbsp;/&nbsp;' + item.original_title : '') +
                    '           <span class="movieYear">&nbsp;(' + item.year + ')</span>' +
                    '       </p>' +
                    '       <div class="movieTab">' +
                    '           <span class="' + (item.type === "电影" ? "movieType1" : "movieType2") + '">' + item.type + '</span>' +
                    tags.join('') +
                    '       </div>' +
                    '       <div class="updateTime">' +
                    '           <label class="common-label">更新时间：</label>' +
                    '           <span class="itemValue">' + item.update_date.slice(0, 20) + '</span>' +
                    '       </div>' +
                    '       <div class="uri">' +
                    '           <label class="common-label">路径：</label>' +
                    '           <span class="itemValue"><a href="' + pre_uri + item.uri + after_uri + '">' + item.uri + '</a></span>' +
                    '       </div>' +
                    '       <div class="doubanRating"><label class="豆瓣评分："></label>' + main.getRateHtml(item.douban_rating) + '</div>' +
                    '   </div>' +
                    '</div>'
            });
        } else {
            main.curPage--;
            $('#moviesListContent_inBottom').remove();
            moviesHtml = "<div id='moviesListContent_inBottom' style='text-align: center'>没有更多了！</div>"
        }

        $('#moviesListContent').append(moviesHtml);
        main.initTagEvent();
    },
    getRateHtml: function (rate) {
        let point = parseFloat(rate / 2).toFixed(1);
        let html = '<span class="rate" title="' + rate + '">';
        for (let i = 1; i <= 5; i++) {

            if (point >= i || (i - point < 0.3)) {
                html += '<i class="fa fa-star" style="color: #f7ba2a"></i>'
            } else if ((parseFloat(i - point).toFixed(1) <= 0.7) && parseFloat(i - point).toFixed(1) >= 0.3) {
                html += '<i class="fa fa-star-half-o" style="color: #f7ba2a"></i>'
            } else {
                html += '<i class="fa fa-star-o" style="color: #f7ba2a"></i>'
            }
        }
        html += '&nbsp;&nbsp;' + rate + '</span>';
        return html;
    },
    formatTime: function (dateStr, fmt) {
        fmt = fmt || 'yyyy-MM-dd hh:mm:ss';
        let date = new Date(dateStr);
        if (/(y+)/.test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
        }
        let o = {
            'M+': date.getMonth() + 1,
            'd+': date.getDate(),
            'h+': date.getHours(),
            'm+': date.getMinutes(),
            's+': date.getSeconds()
        };
        for (let k in o) {
            if (new RegExp("(" + k + ")").test(fmt)) {
                var str = o[k] + '';
                fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? str : padLeftZero(str))
            }
        }
        return fmt;

        function padLeftZero(str) {
            return ('00' + str).substr(str.length)
        }
    },
    reset:function () {
        this.orderBy = '';
        this.orderType = 'asc';
        this.queryYear = '';
        this.curPage = 1;
        this.queryTags = [];

        $('#queryInput').val('');
        $('#selectedTags,#menuSelectedTags').html('');
        $('.orderMenu li .fa').remove();
        $('.orderMenu li').removeClass('active');
        this.getData()
    }
};

function sleep(time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

function loading() {
    $('#moviesListContent')[0].style.display = 'none';

    $(parent.document).find('.loading-flash').remove();
    $(parent.document).find('body').append(
        '<div class="loading-flash" style="top:60px;left: 45%">' +
        '   <i class="fa fa-spinner fa-pulse fa-3x"></i>' +
        '</div>');
}

function unloading() {
    sleep(500).then(() => {
        $(parent.document).find('.loading-flash').remove();
        $('#moviesListContent').fadeIn();

    })
}
