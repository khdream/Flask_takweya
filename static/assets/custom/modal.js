$(function(){
    setModalEvent();
});
function setModalEvent(){
    $(".tomodal-img").off();
    $(".tomodal-img").click(function(){
        $("#img_modal").css("display", 'block');
        $("#img_modal .modal-content").attr("src", $(this).attr("src"));
    })
    $("#img_modal .close").click(function(){
        $("#img_modal").css("display", 'none');
    })
}
var modal = document.getElementById("img_Modal");
function alertInfo(msg){
    $.confirm({
        title: 'Info!',
        content: msg,
        columnClass: 'small',
        type: 'orange',
        typeAnimated: true,
        closeIcon: true,
        buttons: {
            ok: {
                text: 'OK',
                btnClass: 'btn-purple px-5',
            }
        }
    });
}
function alertSuccess(msg){
    $.confirm({
        title: 'Success!',
        content: msg,
        columnClass: 'small',
        type: 'blue',
        typeAnimated: true,
        closeIcon: true,
        buttons: {
            ok: {
                text: 'OK',
                btnClass: 'btn-blue px-5',
            }
        }
    });
}
function alertError(msg){
    $.confirm({
        title: 'Error!',
        content: msg,
        columnClass: 'small',
        type: 'red',
        typeAnimated: true,
        closeIcon: true,
        buttons: {
            ok: {
                text: 'OK',
                btnClass: 'btn-red px-5',
            }
        }
    });
}