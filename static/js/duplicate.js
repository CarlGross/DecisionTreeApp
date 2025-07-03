
function duplicate(){
    const best = document.getElementById('best_case');
    const realistic = document.getElementById('realistic_case');
    const worst = document.getElementById('worst_case');
    const best_realistic = document.getElementById('best_realistic');
    const worst_realistic = document.getElementById('worst_realistic');
    if (best_realistic.checked){
        realistic.value = best.value;
        realistic.disabled = true;
    }
    else {
        realistic.disabled = false;
    }
    if (worst_realistic.checked) {
        worst.value = realistic.value;
        worst.disabled = true;
    }
    else {
        worst.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
document.getElementById('best_realistic').addEventListener('input', duplicate);
document.getElementById('worst_realistic').addEventListener('input', duplicate);
document.getElementById('best_case').addEventListener('input', duplicate);
document.getElementById('realistic_case').addEventListener('input', duplicate);
document.getElementById('form').addEventListener('submit', () => {
    document.getElementById('realistic_case').disabled = false;
    document.getElementById('worst_case').disabled = false;
})
});

