// Main JavaScript for AI-Powered Resume Screener

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // File input custom styling
    const fileInputs = document.querySelectorAll('.custom-file-input');
    fileInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const fileName = this.files[0].name;
            const nextSibling = this.nextElementSibling;
            nextSibling.innerText = fileName;
        });
    });

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });

    // Skills tag input enhancement
    const skillsInput = document.getElementById('skills-input');
    if (skillsInput) {
        const skillsContainer = document.getElementById('skills-container');
        const skillsHiddenInput = document.getElementById('skills');
        const skillsList = [];

        // Function to render skills tags
        function renderSkills() {
            skillsContainer.innerHTML = '';
            skillsList.forEach((skill, index) => {
                const tag = document.createElement('span');
                tag.className = 'badge bg-primary me-2 mb-2';
                tag.innerHTML = `${skill} <button type="button" class="btn-close btn-close-white" data-index="${index}"></button>`;
                skillsContainer.appendChild(tag);
            });
            skillsHiddenInput.value = skillsList.join(',');
        }

        // Add skill when pressing Enter
        skillsInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && this.value.trim() !== '') {
                e.preventDefault();
                const skill = this.value.trim();
                if (!skillsList.includes(skill)) {
                    skillsList.push(skill);
                    renderSkills();
                }
                this.value = '';
            }
        });

        // Remove skill when clicking the close button
        skillsContainer.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn-close')) {
                const index = parseInt(e.target.getAttribute('data-index'));
                skillsList.splice(index, 1);
                renderSkills();
            }
        });

        // Initialize from existing value
        if (skillsHiddenInput.value) {
            skillsList.push(...skillsHiddenInput.value.split(','));
            renderSkills();
        }
    }

    // Match score animation
    const matchScoreElement = document.getElementById('match-score');
    if (matchScoreElement) {
        const targetScore = parseFloat(matchScoreElement.getAttribute('data-score'));
        let currentScore = 0;
        const duration = 1500; // milliseconds
        const interval = 10; // milliseconds
        const steps = duration / interval;
        const increment = targetScore / steps;

        const timer = setInterval(() => {
            currentScore += increment;
            if (currentScore >= targetScore) {
                currentScore = targetScore;
                clearInterval(timer);
            }
            matchScoreElement.textContent = currentScore.toFixed(1) + '%';
        }, interval);
    }
});
