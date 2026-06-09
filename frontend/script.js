const API_URL = 'https://ai-proposal-writer-api.onrender.com/generate-proposal';
const SCOPE_API_URL = 'https://ai-proposal-writer-api.onrender.com/generate-scope';

// DOM Elements
const tabs = document.querySelectorAll('.tab-btn');
const formTitle = document.getElementById('form-title');
const outputTitle = document.getElementById('output-title');
const clientNameGroup = document.getElementById('client-name-group');
const proposalMetaRow = document.getElementById('proposal-meta-row');

const form = document.getElementById('proposal-form');
const generateBtn = document.getElementById('generate-btn');
const btnText = document.querySelector('.btn-text');
const spinner = document.querySelector('.spinner');
const errorMessage = document.getElementById('error-message');

const emptyState = document.getElementById('empty-state');
const proposalOutput = document.getElementById('proposal-output');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');
const pdfBtn = document.getElementById('pdf-btn');

const logoInput = document.getElementById('company_logo');
const pdfLogoPreview = document.getElementById('pdf-logo-preview');

let rawProposalText = '';
let logoBase64 = '';
let currentMode = 'proposal'; // 'proposal' or 'scope'

// Tab Switching
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentMode = tab.dataset.tab;

        // Update UI based on mode
        if (currentMode === 'scope') {
            formTitle.textContent = 'Scope Details';
            outputTitle.textContent = 'Generated Technical Scope';
            clientNameGroup.classList.add('hidden');
            proposalMetaRow.classList.add('hidden');
            document.getElementById('client_name').required = false;
            document.getElementById('budget').required = false;
            document.getElementById('timeline').required = false;
            btnText.textContent = 'Generate Scope';
        } else {
            formTitle.textContent = 'Project Details';
            outputTitle.textContent = 'Generated Proposal';
            clientNameGroup.classList.remove('hidden');
            proposalMetaRow.classList.remove('hidden');
            document.getElementById('client_name').required = true;
            document.getElementById('budget').required = true;
            document.getElementById('timeline').required = true;
            btnText.textContent = 'Generate Proposal';
        }
    });
});

// Handle Logo Upload
logoInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            logoBase64 = event.target.result;
            pdfLogoPreview.src = logoBase64;
            pdfLogoPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        logoBase64 = '';
        pdfLogoPreview.src = '';
        pdfLogoPreview.style.display = 'none';
    }
});

// Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(form);
    const data = {
        project_name: formData.get('project_name'),
        project_description: formData.get('project_description'),
        template: formData.get('proposal_template'),
        additional_notes: formData.get('additional_notes')
    };

    if (currentMode === 'proposal') {
        data.client_name = formData.get('client_name');
        data.budget = formData.get('budget');
        data.timeline = formData.get('timeline');
    }

    // UI state to loading
    setLoadingState(true);
    errorMessage.classList.add('hidden');
    emptyState.classList.add('hidden');
    proposalOutput.classList.add('hidden');
    
    // Disable actions
    copyBtn.disabled = true;
    downloadBtn.disabled = true;
    pdfBtn.disabled = true;

    // Timeout controller (30 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
        const url = currentMode === 'proposal' ? API_URL : SCOPE_API_URL;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            let errorDetail = `Failed to generate ${currentMode}`;
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) {
                errorDetail = `Server Error: ${response.status} ${response.statusText}`;
            }
            throw new Error(errorDetail);
        }

        const result = await response.json();
        
        rawProposalText = currentMode === 'proposal' ? result.proposal : result.scope;
        
        if (!rawProposalText) {
            throw new Error('Received an invalid response from the server.');
        }

        // Render markdown to HTML
        proposalOutput.innerHTML = marked.parse(rawProposalText);
        proposalOutput.classList.remove('hidden');

        // Enable actions
        copyBtn.disabled = false;
        downloadBtn.disabled = false;
        pdfBtn.disabled = false;

    } catch (error) {
        if (error.name === 'AbortError') {
            errorMessage.textContent = 'Request timed out. The server took too long to respond. Please try again.';
        } else if (error.message.includes('Failed to fetch')) {
            errorMessage.textContent = 'Network error. Please check your internet connection or ensure the backend is running.';
        } else {
            errorMessage.textContent = error.message;
        }
        errorMessage.classList.remove('hidden');
        emptyState.classList.remove('hidden');
    } finally {
        setLoadingState(false);
    }
});

function setLoadingState(isLoading) {
    if (isLoading) {
        generateBtn.disabled = true;
        btnText.textContent = currentMode === 'proposal' ? 'Generating Proposal...' : 'Generating Scope...';
        spinner.classList.remove('hidden');
    } else {
        generateBtn.disabled = false;
        btnText.textContent = currentMode === 'proposal' ? 'Generate Proposal' : 'Generate Scope';
        spinner.classList.add('hidden');
    }
}

// Copy functionality
copyBtn.addEventListener('click', async () => {
    if (!rawProposalText) return;
    
    try {
        await navigator.clipboard.writeText(rawProposalText);
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
        }, 2000);
    } catch (err) {
        console.error('Failed to copy text: ', err);
        alert('Failed to copy to clipboard.');
    }
});

// Download functionality
downloadBtn.addEventListener('click', () => {
    if (!rawProposalText) return;

    const blob = new Blob([rawProposalText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    
    // Create a safe filename based on project name
    const projectName = document.getElementById('project_name').value || 'project';
    const safeName = projectName.toLowerCase().replace(/[^a-z0-9]/g, '-');
    const type = currentMode === 'proposal' ? 'proposal' : 'scope';
    
    a.href = url;
    a.download = `${type}-${safeName}.txt`;
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});

// PDF functionality
pdfBtn.addEventListener('click', async () => {
    if (!rawProposalText) return;

    const projectName = document.getElementById('project_name').value || 'Project';
    const clientName = document.getElementById('client_name').value || 'Client';
    const date = new Date().toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });

    // Populate Template
    document.getElementById('pdf-project-name').textContent = projectName;
    document.getElementById('pdf-client-name').textContent = clientName;
    document.getElementById('pdf-date').textContent = date;
    
    // Update Header and Prepared For based on mode
    const headerTitle = document.getElementById('pdf-header-title');
    const preparedForLine = document.getElementById('pdf-prepared-for-line');
    
    if (currentMode === 'scope') {
        headerTitle.textContent = 'TECHNICAL SCOPE';
        preparedForLine.style.display = 'none';
    } else {
        headerTitle.textContent = 'PROPOSAL';
        preparedForLine.style.display = 'block';
    }
    
    const bodyContent = document.getElementById('pdf-body-content');
    bodyContent.innerHTML = marked.parse(rawProposalText);

    // PDF Options
    const opt = {
        margin: 0,
        filename: `${currentMode}-${projectName.toLowerCase().replace(/[^a-z0-9]/g, '-')}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, logging: false },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' },
        pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
    };

    const element = document.getElementById('pdf-template');
    element.style.display = 'block'; // Temporarily show for capture

    try {
        pdfBtn.disabled = true;
        const originalText = pdfBtn.innerHTML;
        pdfBtn.innerHTML = '<span class="spinner" style="border-top-color: var(--primary-color);"></span> Preparing...';

        await html2pdf().set(opt).from(element).save();

        pdfBtn.innerHTML = originalText;
    } catch (err) {
        console.error('PDF generation failed:', err);
        alert('Failed to generate PDF. Please try again.');
    } finally {
        element.style.display = 'none';
        pdfBtn.disabled = false;
    }
});
