/**
 * NeuroStim Dashboard - MQTT Controller
 * Main JavaScript Application File
 */

// Global variables declaration
let client; // MQTT client instance
let reconnectTimeout = 2000; // Reconnection delay in milliseconds
let deviceName = ''; // Current device identifier
let hostName; // MQTT server hostname
let port = 9001; // Default MQTT port over WebSocket
let messageCount = 0; // Counter for received messages
let activeChannels = 0; // Count of active channels (value > 0)

// MQTT subscription configuration
let subscribeOptions = {
    qos: 0, // Quality of Service level (0: at most once)
    invocationContext: {foo: true}, // Context passed to callbacks
    onFailure: onConnectionLost, // Failure callback
    timeout: 10 // Connection timeout in seconds
};

// DOM Content Loaded Event
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    updateLogTimes();
});

/**
 * Initialize all event listeners for UI elements
 */
function initializeEventListeners() {
    // Channel sliders event listeners
    document.getElementById('ch1').addEventListener('input', updateChannelValue.bind(null, 'ch1'));
    document.getElementById('ch2').addEventListener('input', updateChannelValue.bind(null, 'ch2'));
    document.getElementById('ch3').addEventListener('input', updateChannelValue.bind(null, 'ch3'));
    document.getElementById('ch4').addEventListener('input', updateChannelValue.bind(null, 'ch4'));
    
    // Channel sliders change event (when user stops dragging)
    document.getElementById('ch1').addEventListener('change', sendChannelChangedCommand);
    document.getElementById('ch2').addEventListener('change', sendChannelChangedCommand);
    document.getElementById('ch3').addEventListener('change', sendChannelChangedCommand);
    document.getElementById('ch4').addEventListener('change', sendChannelChangedCommand);
    
    // Update display values for range inputs
    document.getElementById('ton').addEventListener('input', function() {
        document.getElementById('tonValue').textContent = this.value;
    });
    
    document.getElementById('period').addEventListener('input', function() {
        document.getElementById('periodValue').textContent = this.value;
    });
}

/**
 * Update channel value display in real-time
 * @param {string} channelId - The ID of the channel slider
 */
function updateChannelValue(channelId) {
    const value = document.getElementById(channelId).value;
    document.getElementById(channelId + 'Value').textContent = value;
    
    // Update active channels count
    updateActiveChannelsCount();
}

/**
 * Update the count of active channels (channels with value > 0)
 */
function updateActiveChannelsCount() {
    const channels = ['ch1', 'ch2', 'ch3', 'ch4'];
    activeChannels = channels.filter(ch => document.getElementById(ch).value > 0).length;
    document.getElementById('activeChannels').textContent = `${activeChannels}/4`;
}

/**
 * Establish MQTT connection with the broker
 */
function connectMQTT() {
    // Get connection parameters from UI
    hostName = document.getElementById('mqttHost').value;
    port = document.getElementById('mqttPort').value;
    deviceName = document.getElementById('deviceName').value;
    
    // Update UI to show connecting state
    const statusIndicator = document.getElementById('statusIndicator');
    const connectBtn = document.getElementById('connectBtn');
    
    statusIndicator.className = 'badge bg-warning connecting';
    statusIndicator.innerHTML = '<i class="fas fa-sync-alt me-1"></i> Connecting...';
    connectBtn.disabled = true;
    connectBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Connecting...';
    
    // Generate unique client ID
    const clientId = 'web_client_' + new Date().getTime();
    
    // Create MQTT client instance
    client = new Paho.MQTT.Client(hostName, Number(port), clientId);
    
    // Set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;
    
    // Connection options
    const connectOptions = {
        onSuccess: onConnectSuccess, // Called on successful connection
        onFailure: onConnectFailure, // Called on connection failure
        keepAliveInterval: 30, // Keep-alive interval in seconds
        timeout: 3, // Connection timeout in seconds
        cleanSession: true, // Start with a clean session
        reconnect: true // Enable automatic reconnection
    };
    
    // Attempt connection
    try {
        client.connect(connectOptions);
        updateDeviceStatus('Connecting to MQTT broker...');
    } catch (error) {
        console.error('Connection error:', error);
        onConnectionLost({errorCode: 0, errorMessage: 'Connection failed'});
    }
}

/**
 * Called when MQTT connection is successfully established
 */
function onConnectSuccess() {
    // Update UI to show connected state
    const statusIndicator = document.getElementById('statusIndicator');
    const connectBtn = document.getElementById('connectBtn');
    
    statusIndicator.className = 'badge bg-success connected';
    statusIndicator.innerHTML = '<i class="fas fa-check-circle me-1"></i> Connected';
    connectBtn.disabled = false;
    connectBtn.innerHTML = '<i class="fas fa-link me-2"></i>Connected';
    
    updateDeviceStatus('Connected to MQTT broker');
    updateLastUpdateTime();
    
    // Subscribe to required topics
    subscribeToTopics();
    
    // Send initial configuration command
    sendInitialCommand();
    
    // Add connection success log
    addToLog('commandlog', `[${getCurrentTime()}] Connected to ${hostName}:${port}`);
}

/**
 * Subscribe to all required MQTT topics
 */
function subscribeToTopics() {
    try {
        client.subscribe("newdev", subscribeOptions);
        client.subscribe(`stream/${deviceName}`, subscribeOptions);
        client.subscribe(`status/${deviceName}`, subscribeOptions);
        client.subscribe(`cmd/${deviceName}`, subscribeOptions);
        
        addToLog('commandlog', `[${getCurrentTime()}] Subscribed to device topics`);
    } catch (error) {
        console.error('Subscription error:', error);
    }
}

/**
 * Send initial configuration command to device
 */
function sendInitialCommand() {
    try {
        const message = new Paho.MQTT.Message('{"op": 0}');
        message.destinationName = `cmd/${deviceName}`;
        client.send(message);
        
        addToLog('commandlog', `[${getCurrentTime()}] Sent initial configuration command`);
    } catch (error) {
        console.error('Send error:', error);
    }
}

/**
 * Called when MQTT connection fails
 */
function onConnectFailure(error) {
    console.error('Connection failed:', error);
    onConnectionLost({errorCode: 0, errorMessage: 'Connection failed'});
}

/**
 * Called when MQTT connection is lost
 * @param {Object} responseObject - Object containing error information
 */
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.error('Connection lost:', responseObject.errorMessage);
    }
    
    // Update UI to show disconnected state
    const statusIndicator = document.getElementById('statusIndicator');
    const connectBtn = document.getElementById('connectBtn');
    
    statusIndicator.className = 'badge bg-danger';
    statusIndicator.innerHTML = '<i class="fas fa-times-circle me-1"></i> Disconnected';
    connectBtn.disabled = false;
    connectBtn.innerHTML = '<i class="fas fa-link me-2"></i>Connect to MQTT';
    
    updateDeviceStatus('Disconnected from MQTT broker');
    
    // Attempt reconnection after delay
    setTimeout(() => {
        if (client && !client.isConnected()) {
            connectMQTT();
        }
    }, reconnectTimeout);
}

/**
 * Called when an MQTT message arrives
 * @param {Object} message - The received MQTT message
 */
function onMessageArrived(message) {
    console.log('Message arrived:', message.destinationName, message.payloadString);
    
    // Increment message counter
    messageCount++;
    document.getElementById('totalMessages').textContent = messageCount;
    
    // Update last update time
    updateLastUpdateTime();
    
    // Route message to appropriate log based on topic
    const destination = message.destinationName;
    
    if (destination === `cmd/${deviceName}`) {
        addToLog('commandlog', `[${getCurrentTime()}] ${message.payloadString}`);
    } else if (destination === `stream/${deviceName}`) {
        addToLog('streaminglog', `[${getCurrentTime()}] ${message.payloadString}`);
    } else if (destination === `status/${deviceName}`) {
        addToLog('responselog', `[${getCurrentTime()}] ${message.payloadString}`);
    } else if (destination === 'newdev') {
        addToLog('deviceLog', `[${getCurrentTime()}] ${message.payloadString}`);
    }
}

/**
 * Send command with all channel values and configuration
 */
function sendChannelChangedCommand() {
    if (!client || !client.isConnected()) {
        alert('Please connect to MQTT first!');
        return;
    }
    
    try {
        // Gather all configuration values
        const ton = document.getElementById('ton').value;
        const period = document.getElementById('period').value;
        const ch1 = document.getElementById('ch1').value;
        const ch2 = document.getElementById('ch2').value;
        const ch3 = document.getElementById('ch3').value;
        const ch4 = document.getElementById('ch4').value;
        
        // Construct message payload
        const payload = {
            op: 2,
            parameters: {
                m: `${ch1},${ch2},${ch3},${ch4}`,
                t: ton,
                p: period
            }
        };
        
        // Create and send MQTT message
        const message = new Paho.MQTT.Message(JSON.stringify(payload));
        message.destinationName = `cmd/${deviceName}`;
        client.send(message);
        
        // Log the command
        addToLog('commandlog', `[${getCurrentTime()}] Sent channel values: ${payload.parameters.m}`);
        
        // Update UI
        updateActiveChannelsCount();
        
    } catch (error) {
        console.error('Send command error:', error);
        addToLog('commandlog', `[${getCurrentTime()}] Error: ${error.message}`);
    }
}

/**
 * Send all channels command (manual trigger)
 */
function sendAllChannels() {
    sendChannelChangedCommand();
}

/**
 * Add message to specified log with auto-scroll
 * @param {string} logId - The ID of the log textarea
 * @param {string} message - The message to add
 */
function addToLog(logId, message) {
    const log = document.getElementById(logId);
    if (log) {
        log.value += message + '\n';
        // Auto-scroll to bottom
        log.scrollTop = log.scrollHeight;
    }
}

/**
 * Clear specific log
 * @param {string} logId - The ID of the log to clear
 */
function clearLog(logId) {
    const log = document.getElementById(logId);
    if (log) {
        log.value = '';
    }
}

/**
 * Clear all logs
 */
function clearAllLogs() {
    ['commandlog', 'responselog', 'streaminglog', 'deviceLog'].forEach(clearLog);
}

/**
 * Get current time formatted as HH:MM:SS
 * @returns {string} Formatted time string
 */
function getCurrentTime() {
    const now = new Date();
    return now.toTimeString().split(' ')[0];
}

/**
 * Update last update time display
 */
function updateLastUpdateTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('lastUpdate').textContent = timeString;
}

/**
 * Update device status display
 * @param {string} status - Status message to display
 */
function updateDeviceStatus(status) {
    document.getElementById('deviceStatus').textContent = status;
}

/**
 * Update all log timestamps periodically (optional)
 */
function updateLogTimes() {
    // This function can be extended to update timestamps if needed
    setInterval(() => {
        // Example: Update connection quality indicator
        if (client && client.isConnected()) {
            document.getElementById('connectionQuality').textContent = 'Good';
        }
    }, 5000);
}

// Make functions available globally
window.connectMQTT = connectMQTT;
window.sendChannelChangedCommand = sendChannelChangedCommand;
window.sendAllChannels = sendAllChannels;
window.clearLog = clearLog;
window.clearAllLogs = clearAllLogs;