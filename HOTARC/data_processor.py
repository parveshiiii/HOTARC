import numpy as np
import logging
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from keras.models import Model
from keras.layers import Input, Dense
from keras.optimizers import Adam

class DataProcessor:
    def __init__(self):
        logging.basicConfig(filename='data_processor.log', level=logging.INFO)

    def augment_data(self, data):
        augmented_data = self._apply_noise_injection(data)
        augmented_data = self._apply_data_warping(augmented_data)
        augmented_data = self._generate_synthetic_data(augmented_data)
        return augmented_data

    def _apply_noise_injection(self, data, noise_level=0.01):
        noise = np.random.normal(0, noise_level, data.shape)
        noisy_data = data + noise
        logging.info("Applied noise injection.")
        return noisy_data

    def _apply_data_warping(self, data, warping_factor=0.01):
        warped_data = data + warping_factor * np.sin(data)
        logging.info("Applied data warping.")
        return warped_data

    def _generate_synthetic_data(self, data, num_samples=100):
        synthetic_data = np.random.choice(data.flatten(), (num_samples, data.shape[1]))
        logging.info("Generated synthetic data.")
        return np.vstack([data, synthetic_data])

    def detect_anomalies(self, data, method='isolation_forest'):
        if method == 'isolation_forest':
            return self._detect_anomalies_isolation_forest(data)
        elif method == 'dbscan':
            return self._detect_anomalies_dbscan(data)
        elif method == 'autoencoder':
            return self._detect_anomalies_autoencoder(data)
        else:
            logging.error(f"Unknown anomaly detection method: {method}")
            return None

    def _detect_anomalies_isolation_forest(self, data):
        clf = IsolationForest(contamination=0.1)
        clf.fit(data)
        anomalies = clf.predict(data)
        anomaly_indices = np.where(anomalies == -1)[0]
        logging.info(f"Detected {len(anomaly_indices)} anomalies using Isolation Forest.")
        return anomaly_indices

    def _detect_anomalies_dbscan(self, data, eps=0.5, min_samples=5):
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data)
        db = DBSCAN(eps=eps, min_samples=min_samples).fit(data_scaled)
        labels = db.labels_
        anomaly_indices = np.where(labels == -1)[0]
        logging.info(f"Detected {len(anomaly_indices)} anomalies using DBSCAN.")
        return anomaly_indices

    def _detect_anomalies_autoencoder(self, data, epochs=50, batch_size=32):
        input_dim = data.shape[1]
        encoding_dim = input_dim // 2

        input_layer = Input(shape=(input_dim,))
        encoded = Dense(encoding_dim, activation='relu')(input_layer)
        decoded = Dense(input_dim, activation='sigmoid')(encoded)

        autoencoder = Model(input_layer, decoded)
        autoencoder.compile(optimizer=Adam(), loss='mean_squared_error')

        autoencoder.fit(data, data, epochs=epochs, batch_size=batch_size, shuffle=True, verbose=0)
        predictions = autoencoder.predict(data)
        mse = np.mean(np.power(data - predictions, 2), axis=1)
        anomaly_indices = np.where(mse > np.percentile(mse, 95))[0]
        logging.info(f"Detected {len(anomaly_indices)} anomalies using Autoencoder.")
        return anomaly_indices