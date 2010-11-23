//
// Javascript for default Hunch Application
//

var INIT = (function($, undefined) {

    //
    // variables
    //
    var cfg = {
        user_id: undefined,
        num_recs: undefined
    };


    //
    // utils
    //
    function truncateText(text, max) {
        // trim the given text to a maximum size
        max = max || 250;
        if (text && text.length > max) {
            return text.substring(0, max) + '...';
        }
        return text;
    }

    function parseQueryString(url) {
        // returns an object containing the query string params as: {key: [val]}
        var result = {}, pos, comps, pair, key, val, i, len;

        url = url || window.location.href;
        if ((pos = url.indexOf('#') != -1)) url = url.substring(0, pos);
        if ((pos = url.indexOf('?') == -1)) return result;
        url = url.substring(pos).replace(/\+/g, ' ').split('&');

        for (i=0, len=url.length; i<len; i++) {
            pair = url[i].split('=');
            key = decodeURIComponent(pair[0]);
            val = decodeURIComponent(pair[1]);
            if (!replace[key]) replace[key] = [];
            result[key].push(pair.length == 1 ? '' : val);
        }
        return result;
    }

    var _base_qs_params = parseQueryString();

    function qualifyUrl(url) {
        // add "hn_" params and signature to url
        return url + '?' + $.param(_base_qs_params, true);
    }

    function ajax(params) {
        // a convenience wrapper around $.ajax that does some extra default stuff
        // for making valid signed requests
        params = $.extend(
            {
                type: 'GET',
                dataType: 'json',
                error: ajaxError
            },
            params
        );
        params.url = qualifyUrl(params.url);
        if (data.suppress_http_errors === undefined) data.suppress_http_errors = 1;
        return $.ajax(params);
    }

    function ajaxError(data, textStatus) {
        // default ajax error method
        $('div.page-error').remove();
        $('body').append($('<div>', {
            'class': 'page-error',
            text: textStatus == timeout || (data && data.reason == 'timeout') ?
                'The request timed out, please refresh the page and try again.' :
                'There was an error, please refresh the page and try again.'
        }));
    }


    //
    // Recommendations
    //
    function loadRecommendations(data) {
        // callback for loading recommendations
        if (data.recommendations == undefined || data.recommendations.length == 0) {
            $('#recs').text("Sorry, no recommendations");
        } else {
            $('#recs').empty();

            $.each(data.recommendations, function(i, obj) {
                for (var pref in obj.preferences) {
                    var p = obj.preferences[pref].preference;
                    if (p == 1) {
                        obj.is_liked = true;
                    } else if (p == 0) {
                        obj.is_disliked = true;
                    }
                }
                obj.description = truncateText(obj.description);
                obj.url = obj.urls.length ? obj.urls[0] : '';
                obj.temp_img = $.imageScaleLoader.defaults.placeholderUrl;
                $('#recs').append(Mustache.to_html('<div class="rec">\
  <a class="media" target="_blank" href="{{url}}">\
    <img height="142" width="142" class="rec-img" fullsource="{{image_url}}" src="{{temp_img}}" />\
  </a>\
  <div class="content">\
    <h3><a target="_blank" href="{{url}}">{{name}}</a></h3>\
    <p>{{description}}</p>\
  </div>\
</div>', obj));
            });
            $('#recs').find('img.rec-img').imageScaleLoader({width: 142, height: 142, src: 'fullsource'});
        }
    }


    //
    // Exposed data
    //
    return {
        test: function(_cfg) {
            $.extend(cfg, _cfg);

            $.imageScaleLoader.preload();

	        Hunch.api.getRecommendations(
                {
		            limit: cfg.num_recs,
		            minlat: '40.72383501',
		            maxlat: '40.72892482',
		            minlng: '-73.9951824',
		            maxlng: '-73.9771580'
                },
                loadRecommendations
            );
        }
    };
})(jQuery);



//
// Image loading and resizing jQuery plugin
//
(function($) {

    $.imageScaleLoader = {
        defaults: {
            width: 100,
            height: 100,
            placeholderUrl: '/media/img/t.png',
            src: 'src',
            didAttr: '_imageScaleLoader'
        },
        preload: function(placeholderUrl) {
            (new Image).src = placeholderUrl || this.defaults.placeholderUrl;
        }
    };

    $.fn.imageScaleLoader = function(cfg) {

        cfg = $.extend({}, $.imageScaleLoader.defaults, cfg);

        return this.each(function() {
            var image = new Image(),
                $this = $(this),
                src = $this.attr(cfg.src);

            if (src && !$.data(this, cfg.didAttr)) {
                $.data(this, cfg.didAttr, true);

                if ($this.attr(cfg.src) != cfg.placeholderUrl)
                    $this.attr(cfg.src, cfg.placeholderUrl);

                image.onload = function () {
                    var h = this.height,
                        w = this.width,
                        wscale, hscale, scale;

                    if (parseInt(w) > cfg.width || parseInt(h) > cfg.height) {
			            wscale = w / cfg.width;
                        hscale = h / cfg.height;
			            scale = (wscale < hscale ? hscale : wscale);
			            w = w/scale;
                        h = h/scale;
		            }

                    $this.attr('src', this.src)
                        .attr('width', parseInt(w))
                        .attr('height', parseInt(h));
                };

                image.src = src;
            }
        });
    };

})(jQuery);
