const API_URL = 'https://ai-proposal-writer-api.onrender.com/generate-proposal';

// DOM Elements
const form = document.getElementById('proposal-form');
const generateBtn = document.getElementById('generate-btn');
const btnText = document.querySelector('.btn-text');
const spinner = document.querySelector('.spinner');
const errorMessage = document.getElementById('error-message');

const emptyState = document.getElementById('empty-state');
const proposalOutput = document.getElementById('proposal-output');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');

let rawProposalText = '';

// Form Submission
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(form);
    const data = {
        client_name: formData.get('client_name'),
        project_name: formData.get('project_name'),
        project_description: formData.get('project_description'),
        budget: formData.get('budget'),
        timeline: formData.get('timeline'),
        additional_notes: formData.get('additional_notes')
    };

    // UI state to loading
    setLoadingState(true);
    errorMessage.classList.add('hidden');
    emptyState.classList.add('hidden');
    proposalOutput.classList.add('hidden');
    
    // Disable actions
    copyBtn.disabled = true;
    downloadBtn.disabled = true;

    // Timeout controller (30 seconds)
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            let errorDetail = 'Failed to generate proposal';
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) {
                errorDetail = `Server Error: ${response.status} ${response.statusText}`;
            }
            throw new Error(errorDetail);
        }

        const result = await response.json();
        
        if (!result || !result.proposal) {
            throw new Error('Received an invalid response from the server.');
        }

        rawProposalText = result.proposal;
        
        // Render markdown to HTML
        proposalOutput.innerHTML = marked.parse(rawProposalText);
        proposalOutput.classList.remove('hidden');

        // Enable actions
        copyBtn.disabled = false;
        downloadBtn.disabled = false;

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
        btnText.textContent = 'Generating...';
        spinner.classList.remove('hidden');
    } else {
        generateBtn.disabled = false;
        btnText.textContent = 'Generate Proposal';
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
    
    a.href = url;
    a.download = `proposal-${safeName}.txt`;
    document.body.appendChild(a);
    a.click();
    
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
});
