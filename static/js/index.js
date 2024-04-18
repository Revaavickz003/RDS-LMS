const sideLinks = document.querySelectorAll('.sidebar .side-menu li a:not(.logout)');

sideLinks.forEach(item => {
    const li = item.parentElement;
    item.addEventListener('click', () => {
        sideLinks.forEach(i => {
            i.parentElement.classList.remove('active');
        })
        li.classList.add('active');
    })
});

const menuBar = document.querySelector('.content nav .bx.bx-menu');
const sideBar = document.querySelector('.sidebar');

menuBar.addEventListener('click', () => {
    sideBar.classList.toggle('close');
});

const searchBtn = document.querySelector('.content nav form .form-input button');
const searchBtnIcon = document.querySelector('.content nav form .form-input button .bx');
const searchForm = document.querySelector('.content nav form');

searchBtn.addEventListener('click', function (e) {
    if (window.innerWidth < 576) {
        e.preventDefault;
        searchForm.classList.toggle('show');
        if (searchForm.classList.contains('show')) {
            searchBtnIcon.classList.replace('bx-search', 'bx-x');
        } else {
            searchBtnIcon.classList.replace('bx-x', 'bx-search');
        }
    }
});

window.addEventListener('resize', () => {
    if (window.innerWidth < 768) {
        sideBar.classList.add('close');
    } else {
        sideBar.classList.remove('close');
    }
    if (window.innerWidth > 576) {
        searchBtnIcon.classList.replace('bx-x', 'bx-search');
        searchForm.classList.remove('show');
    }
});

const toggler = document.getElementById('theme-toggle');

toggler.addEventListener('change', function () {
    if (this.checked) {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const bxplus_btn = document.getElementById('bxplus');
    const leads_container = document.getElementById('leads-container');
    const view_leads = document.getElementById('view-leads');
    const report = document.getElementById('report');
    const newlead = document.getElementById('leads-big-container');
    const dropcontainer = document.getElementById('dropcontainer');

    bxplus_btn.addEventListener('click', () => {
        leads_container.classList.toggle('container-hidden');
        view_leads.classList.toggle('container-hidden');
        report.classList.toggle('container-hidden');
        newlead.classList.toggle('container-hidden');
        dropcontainer.classList.toggle('container-hidden');
    });
});


const notification = document.getElementById('notification');
const notificationcontainer = document.getElementById('notification-container');

notification.addEventListener('click',()=>{
    notificationcontainer.classList.toggle('show')
})
