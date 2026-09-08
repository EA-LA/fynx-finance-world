document.querySelectorAll('[data-menu-toggle]').forEach((button)=>button.addEventListener('click',()=>{
  const menu=document.querySelector('.nav-links');
  const open=menu?.classList.toggle('open');
  button.setAttribute('aria-expanded',String(Boolean(open)));
}));

const current=(location.pathname.split('/').pop()||'index.html');
document.querySelectorAll('.nav-links a').forEach((link)=>{
  if(link.getAttribute('href')===current) link.setAttribute('aria-current','page');
});
