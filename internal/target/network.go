package target

type NetworkTarget struct {
	Name    string
	Network string
	Address string
	Port    int
	Safe    bool
}

func (t *NetworkTarget) Check() (bool, error) {
	return true, nil
}
