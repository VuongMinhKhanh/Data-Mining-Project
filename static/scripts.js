$(document).ready(function(){
            // Hiển thị modal và ẩn pagination
            $('#learn-more').on('click', function() {
                $('#algorithmModal').css('display', 'flex');
                $('.swiper-pagination').css('display', 'none'); // Ẩn pagination khi modal hiện
            });

            // Đóng modal và hiển thị lại pagination
            $('.close').on('click', function() {
                $('#algorithmModal').css('display', 'none');
                $('.swiper-pagination').css('display', 'block'); // Hiển thị lại pagination khi modal đóng
            });

            // Đóng modal và trả lại trang chủ
            $(window).on('click', function(event) {
                if ($(event.target).is('#algorithmModal')) {
                    $('#algorithmModal').css('display', 'none');
                }
            });


            $('nav ul li a').on('click', function(event) {
                event.preventDefault();
                $('html, body').animate({
                    scrollTop: $($(this).attr('href')).offset().top
                }, 500);
            });


            $('.algorithm-section .btn').on('mouseover', function() {
                $(this).css('background-color', '#ff4081');
            }).on('mouseout', function() {
                $(this).css('background-color', '#6200ea');
            });

            const swiper = new Swiper('.swiper-container', {
                loop: true,
                autoplay: {
                    delay: 1000,
                    disableOnInteraction: false,
                },
                pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                },
                effect: 'slide',
            });
        });