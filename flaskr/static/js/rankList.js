var now = new Date();


axios.get("http://localhost:8088/api/rank")
    .then(function (response) {
        console.log(response)
        var rankList = new Vue({
            el: "#rankList",
            data: {
                rankListGet:response.data,
                rank_details: [{
                    title: "xx",
                    play_url: "bili.com",
                    heat: "1.3w"
                }]
            },
            methods: {
                getPlayUrl: function (item, index) {
                    var urlList = item.play_url;
                    // var firstKey = Object.keys(urlList)[0];
                    // return urlList[firstKey];
                    return urlList;
                },
            }
        })
    })
