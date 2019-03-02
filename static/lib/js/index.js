new Vue({
    el: '#app',
    data:{
        backgroundimg:'../../static/res/backgroundimg/backgroudimgheight.jpg',
        screenwidth:100,
        screenheight:100,
    },
    computed:{
        widthchange:function(){
            return this.screenwidth;
        },
        heightchange:function(){
            return this.screenheight;
        },
    },
    mounted () {
        //适配主页背景图片格式
        this.screenwidth = window.innerWidth;
        this.screenheight = window.innerHeight;
        if(this.screenwidth/this.screenheight>1){
            this.backgroundimg = "../../static/res/backgroundimg/backgroundimgwidth.jpeg"
        }
        else{
            this.backgroundimg = '../../static/res/backgroundimg/backgroudimgheight.jpg'
        }
    },
    methods: { 
        //适配主页背景图片格式
        resize () {
            this.screenwidth = window.innerWidth;
            this.screenheight = window.innerHeight;
            if(this.screenwidth/this.screenheight>1){
                this.backgroundimg = "../../static/res/backgroundimg/backgroundimgwidth.jpeg"
            }
            else{
                this.backgroundimg = '../../static/res/backgroundimg/backgroudimgheight.jpg'
            }
        },
    },
});