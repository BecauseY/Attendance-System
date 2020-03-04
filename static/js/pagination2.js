function firstPage2(){
    hide2();
    currPageNum2 = 1;
    showCurrPage2(currPageNum2);
    showTotalPage2();
    for(i = 1; i < pageCount2 + 1; i++){
        blockTable2.rows[i].style.display = "";
    }

    firstText2();
    preText2();
    nextLink2();
    lastLink2();
}

function prePage2(){
    hide2();
    currPageNum2--;
    showCurrPage2(currPageNum2);
    showTotalPage2();
    var firstR = firstRow2(currPageNum2);
    var lastR = lastRow2(firstR);
    for(i = firstR; i < lastR; i++){
        blockTable2.rows[i].style.display = "";
    }

    if(1 == currPageNum2){
        firstText2();
        preText2();
        nextLink2();
        lastLink2();
    }else if(pageNum2 == currPageNum2){
        preLink2();
        firstLink2();
        nextText2();
        lastText2();
    }else{
        firstLink2();
        preLink2();
        nextLink2();
        lastLink2();
    }

}

function nextPage2(){
    hide2();
    currPageNum2++;
    showCurrPage2(currPageNum2);
    showTotalPage2();
    var firstR = firstRow2(currPageNum2);
    var lastR = lastRow2(firstR);
    for(i = firstR; i < lastR; i ++){
        blockTable2.rows[i].style.display = "";
    }

    if(1 == currPageNum2){
        firstText2();
        preText2();
        nextLink2();
        lastLink2();
    }else if(pageNum2 == currPageNum2){
        preLink2();
        firstLink2();
        nextText2();
        lastText2();
    }else{
        firstLink2();
        preLink2();
        nextLink2();
        lastLink2();
    }
}

function lastPage2(){
    hide2();
    currPageNum2 = pageNum2;
    showCurrPage2(currPageNum2);
    showTotalPage2();
    var firstR = firstRow2(currPageNum2);
    for(i = firstR; i < numCount2 + 1; i++){
        blockTable2.rows[i].style.display = "";
    }

    firstLink2();
    preLink2();
    nextText2();
    lastText2();
}

// 计算将要显示的页面的首行和尾行
function firstRow2(currPageNum2){
    return pageCount2*(currPageNum2 - 1) + 1;
}

function lastRow2(firstRow){
    var lastRow = firstRow + pageCount2;
    if(lastRow > numCount2 + 1){
        lastRow = numCount2 + 1;
    }
    return lastRow;
}

function showCurrPage2(cpn){
    currPageSpan2.innerHTML = cpn;
}

function showTotalPage2(){
    pageNumSpan2.innerHTML = pageNum2;
}

//隐藏所有行
function hide2(){
    for(var i = 1; i < numCount2 + 1; i ++){
        blockTable2.rows[i].style.display = "none";
    }
}

//控制首页等功能的显示与不显示
function firstLink2(){firstSpan2.innerHTML = "<a href='javascript:firstPage2();'>First</a>";}
function firstText2(){firstSpan2.innerHTML = "First";}

function preLink2(){preSpan2.innerHTML = "<a href='javascript:prePage2();'>Pre</a>";}
function preText2(){preSpan2.innerHTML = "Pre";}

function nextLink2(){nextSpan2.innerHTML = "<a href='javascript:nextPage2();'>Next</a>";}
function nextText2(){nextSpan2.innerHTML = "Next";}

function lastLink2(){lastSpan2.innerHTML = "<a href='javascript:lastPage2();'>Last</a>";}
function lastText2(){lastSpan2.innerHTML = "Last";}