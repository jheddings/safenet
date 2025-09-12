package main

import (
	"os"

	"github.com/jheddings/safenet/internal/target"
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"github.com/spf13/viper"
)

// Config represents the application configuration structure
type Config struct {
	Websites []target.WebsiteTarget `mapstructure:"websites"`
	Systems  []target.SystemTarget  `mapstructure:"systems"`
	Networks []target.NetworkTarget `mapstructure:"networks"`
}

var cfg Config

func init() {
	viper.SetEnvPrefix("SAFENET")
	viper.AutomaticEnv()
	viper.SetConfigFile("safenet.yaml")
	viper.SetConfigType("yaml")

	if err := viper.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); ok {
			log.Printf("Config file not found; using defaults")
		} else {
			log.Fatal().Err(err).Msgf("Error reading config file: %v", err)
		}
	}

	// Unmarshal the configuration into our struct
	if err := viper.Unmarshal(&cfg); err != nil {
		log.Fatal().Err(err).Msgf("Error unmarshaling config: %v", err)
	}

	initLogging()
}

func initLogging() {
	zerolog.SetGlobalLevel(zerolog.InfoLevel)
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})
}

func main() {
	// Example usage of the loaded configuration
	log.Info().Msgf("Loaded %d websites", len(cfg.Websites))
	log.Info().Msgf("Loaded %d systems", len(cfg.Systems))
	log.Info().Msgf("Loaded %d networks", len(cfg.Networks))

	// Example: Print all website targets
	for _, website := range cfg.Websites {
		log.Info().
			Str("name", website.Name).
			Str("address", website.Address).
			Bool("safe", website.Safe).
			Msg("Website target")
	}

	// Example: Print all system targets
	for _, system := range cfg.Systems {
		log.Info().
			Str("name", system.Name).
			Str("address", system.Address).
			Bool("safe", system.Safe).
			Msg("System target")
	}

	// Example: Print all network targets
	for _, network := range cfg.Networks {
		log.Info().
			Str("name", network.Name).
			Str("network", network.Network).
			Str("address", network.Address).
			Int("port", network.Port).
			Bool("safe", network.Safe).
			Msg("Network target")
	}
}
