const form = document.getElementById('motherForm');
const list = document.getElementById('motherList');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const data = {
        fullName: fullName.value,
        nationalId: nationalId.value,
        dob: dob.value,
        phone: phone.value,
        address: address.value,
        gravidity: gravidity.value,
        parity: parity.value,
        lmp: lmp.value,
        edd: edd.value,
        bloodPressure: bloodPressure.value,
        weight: weight.value,
        bloodGroup: bloodGroup.value,
        hivStatus: hivStatus.value,
        riskFactors: riskFactors.value
    };

    await fetch('/addMother', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    alert("Mother saved!");
    form.reset();
    loadMothers();
});

async function loadMothers() {
    const res = await fetch('/mothers');
    const data = await res.json();
    list.innerHTML = '';

    data.forEach(mother => {
        const li = document.createElement('li');
        li.textContent = `${mother.fullName} - ${mother.phone}`;
        list.appendChild(li);
    });
}

loadMothers();