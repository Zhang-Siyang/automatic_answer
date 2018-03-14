// ==UserScript==
// @name           党的19大精神学习竞赛答题助手
// @author         石成
// @match          *xxjs.dtdjzx.gov.cn/kaishijingsai*
// @namespace      https://github.com/shichengcn/automatic_answer
// @version        0.2
// @description    [答题助手][自动答题]
// @license        MIT
// @supportURL     https://github.com/shichengcn/automatic_answer/issues
// @date           01/11/2018
// @modified       03/13/2018
// ==/UserScript==

var daoshushjian = 30;

function daan(){
    //跨域请求jsonp脚本，执行脚本后获取答案数据,变量名字ans
   $.ajax({
    type : 'get',
    url:'http://shichengcn.me/party_building_automatic_answer/all_answer_set.txt',
    //url:'http://211.87.235.83/movie/all_answer_set.txt',
    cache :false,
    jsonp: "callback",
    jsonpCallback:"success",
    dataType : 'jsonp',
    success:function(data){
         localStorage.setItem('all_ans_Data',JSON.stringify(ans)); //答案缓存
         subjectInfoList=[];
         //console.log(ans);
         atuo_ans();
         simulates_clicking();
    },
    error:function(data){
         localStorage.setItem('all_ans_Data',JSON.stringify(ans)); //答案缓存
         subjectInfoList=[];
         //console.log(ans);
         atuo_ans();
         simulates_clicking();
    }
});
}

function atuo_ans(){
    var subjectInfoList = JSON.parse(localStorage.getItem("all_ans_Data")); //获取答案缓存
    //console.log($('.W_ti_ul li div input'));
    //console.log(subjectInfoList);
    var j = 0;
    var no_ans_number = '';
    var ans_str='';
    var true_id= 0;
    for(var i=0; i<$('.W_ti_ul li div input').length;i=i+4){
        true_id = true_id + 1;
        ans_str='';
        for(var key in subjectInfoList){
            if($('.W_ti_ul li div input')[i].attributes.ids.value == key){
                ans_str =subjectInfoList[key];
                //console.log($('.W_ti_ul li div input')[i].attributes.ids.value);
                //console.log(subjectInfoList[k].id);
                break;
            }
        }
        if (ans_str == ''){
            no_ans_number  = no_ans_number + true_id;
            if( true_id  <20){
                no_ans_number  = no_ans_number + '、';
            }
        }
        else{
             if(ans_str.indexOf("A") >= 0){
                 $('.W_ti_ul li div input')[i].checked = true;
             }
            if(ans_str.indexOf("B") >= 0){
                $('.W_ti_ul li div input')[i+1].checked = true;
            }
            if(ans_str.indexOf("C") >= 0){
                $('.W_ti_ul li div input')[i+2].checked = true;
            }
            if(ans_str.indexOf("D") >= 0){
                $('.W_ti_ul li div input')[i+3].checked = true;
            }
            $('.W_kuan li').eq(j).addClass('activess');
        }
        j = j+1;
        //ans_str = subjectInfoList[j].answer;
        //console.log(subjectInfoList[j].answer);
        //console.log($('.W_ti_ul li div input')[i].attributes.ids.value);
        //console.log(ans_str);
    }
    if(no_ans_number!=''){
        alert("题库中缺少第"+no_ans_number+"题的答案，请手动作答！");
    }
    $("body > div.l_box > div > div.w_loads > div > ul > li:nth-child(1)").addClass('activess');
    $('.W_kuan li').eq(j+1).addClass('activess');
    w_nowNum = w_total-1;
    localStorage.setItem('anniujia',w_nowNum);
    $('.w_btn_tab_down').removeClass('W_bgcol');
    subjectInfoList=[];
}
function simulates_clicking(){
  //模拟点击
 fake_x = [537, 587, 633, 681, 731, 781, 830, 881, 926, 978, 1027, 1077, 1126, 1171, 1224, 1269, 1322, 1370, 1415];
 fake_y = [349, 345, 348, 348, 349, 349, 351, 351, 349, 349, 351, 352, 350, 351, 348, 349, 347, 350, 351];
 my_max = 2;
 my_min = -2;
 for(var j=0; j< fake_x.length;j++){
    fake_x[j] = fake_x[j]+ Math.floor(Math.random()*(my_max-my_min+1)+my_min);
    fake_y[j] =  fake_y[j] +Math.floor(Math.random()*(my_max-my_min+1)+my_min);
    clientXArr.push(fake_x[j]);
	clientXArrY.push(fake_y[j]);
    if(clientXArr.length>=w_total-1){
         for(var i=0,len=arr.length;i<len;i++){
             if(obj[arr[i]]){
                 obj[arr[i]]++;
                 maxArr.push(obj[arr[i]]);
             }
             else{
                 obj[arr[i]]=1;
             }
         }
         maxArr=maxArr.sort(function(x,y){return x-y;});
         repeatX= maxArr.length>0 ? maxArr[maxArr.length-1] : 0 ;//重复x 坐标的次数
     }
}
}
var mytime = 0;
var myjisiqi=setInterval(daojishi,1000);
$('.jiaojuanss').addClass('W_jiaoquancol');
function daojishi(){
    mytime++;
    if(parseInt(mytime)< parseInt(daoshushjian)){
        $(".W_jiaoquancol")["0"].innerText = (parseInt(daoshushjian) - parseInt(mytime)) + "秒可以交卷";
    }else{
            //console.log("检测到全部答完");
            $(".W_jiaoquancol")["0"].innerText = "交卷";
            window.clearInterval(myjisiqi);
           $('.jiaojuanss').removeClass('W_jiaoquancol')	;
    }

}
daan();
